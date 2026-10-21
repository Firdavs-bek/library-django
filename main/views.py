from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Book, Genre, ReadingProgress, User


def index(request):
    books = Book.objects.select_related('genre')
    top = books.order_by('-rating')
    return render(request, 'index.html', {
        'featured': top.first(), 'new': books[:4], 'top': top[:4],
        'book_count': books.count(), 'genre_count': Genre.objects.count(),
    })


def books(request):
    return render(request, 'books.html', {
        'books': Book.objects.select_related('genre'), 'genres': Genre.objects.all(),
        'q': request.GET.get('q', ''),
    })


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('genre'), pk=pk)
    others = list(Book.objects.exclude(pk=pk).select_related('genre'))
    others.sort(key=lambda b: b.genre_id != book.genre_id)      
    progress = None
    if request.user.is_authenticated:
        progress = ReadingProgress.objects.filter(user=request.user, book=book).first()
    percent = round(progress.current_page / progress.total_pages * 100) if progress and progress.total_pages else 0
    return render(request, 'book.html', {'book': book, 'similar': others[:4], 'progress': progress, 'percent': percent})


def read(request, pk):
    book = get_object_or_404(Book, pk=pk)
    pages = list(book.book_pages.all())
    total = len(pages)
    saved = ReadingProgress.objects.filter(user=request.user, book=book).first() if request.user.is_authenticated else None
    try:
        n = int(request.GET.get('page') or (saved.current_page if saved else 1))
    except ValueError:
        n = 1
    n = min(max(n, 1), max(total, 1))
    page = pages[n - 1] if pages else None
    if page and request.user.is_authenticated:                  
        ReadingProgress.objects.update_or_create(
            user=request.user, book=book,
            defaults={'current_page': n, 'total_pages': total, 'finished_at': timezone.now() if n == total else None})
    paragraphs = [p.strip() for p in page.text.split('\n\n') if p.strip()] if page else []
    return render(request, 'read.html', {
        'book': book, 'n': n, 'total': total, 'paragraphs': paragraphs,
        'prev': n - 1 if n > 1 else None, 'next': n + 1 if n < total else None})


def auth_view(request):
    """Bitta sahifada ikkita forma: kirish va ro‘yxatdan o‘tish."""
    if request.user.is_authenticated:
        return redirect('index')
    error, tab = '', 'login'
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        if request.POST.get('action') == 'register':
            tab, name = 'register', request.POST.get('name', '').strip()
            if not name or '@' not in email or len(password) < 6:
                error = 'Ism, togri email va kamida 6 belgili parolni kiriting.'
            elif User.objects.filter(email__iexact=email).exists():
                error = 'Bu email bilan hisob mavjud.'
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
                login(request, user)
                return redirect('index')
        else:
            found = User.objects.filter(email__iexact=email).first()
            user = authenticate(request, username=found.username, password=password) if found else None
            if user:
                login(request, user)
                return redirect('index')
            error = 'Email yoki parol notogri.'
    return render(request, 'login.html', {'error': error, 'tab': tab})


def logout_view(request):
    logout(request)
    return redirect('index')
