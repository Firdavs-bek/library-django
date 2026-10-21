import json
from pathlib import Path

from django.core.management.base import BaseCommand

from main.models import Book, BookPage, Genre


class Command(BaseCommand):
    help = "Namunaviy janrlar va 6 ta hikoyani bazaga qo‘shadi (python manage.py seed)"

    def handle(self, *args, **options):
        data = json.loads((Path(__file__).parent / 'seed_data.json').read_text(encoding='utf-8'))
        genres = {slug: Genre.objects.get_or_create(slug=slug, defaults={'name': v[0]})[0] for slug, v in data['genres'].items()}
        for b in reversed(data['books']):
            book, created = Book.objects.get_or_create(title=b['title'], defaults=dict(
                author=b['author'], genre=genres[b['genre']], year=b['year'], rating=b['rating'],
                description=b['desc'], cover_color=b['color']))
            if created:   # har 2 abzats = 1 sahifa
                for i in range(0, len(b['content']), 2):
                    BookPage.objects.create(book=book, page_number=i // 2 + 1, text='\n\n'.join(b['content'][i:i + 2]))
                book.pages = book.book_pages.count()
                book.save()
        self.stdout.write(self.style.SUCCESS(f"Tayyor: {Book.objects.count()} ta kitob"))
