from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Oddiy foydalanuvchi'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username



class Genre(models.Model):
    slug = models.CharField(max_length=50, unique=True)  
    name = models.CharField(max_length=100)

    ICONS = {'roman': 'bi-heart', 'tarix': 'bi-bank', 'biznes': 'bi-graph-up-arrow',
             'psixologiya': 'bi-lightbulb', 'fantastika': 'bi-stars', 'ilm': 'bi-rocket-takeoff'}

    @property
    def icon(self):   
        return self.ICONS.get(self.slug, 'bi-book')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    year = models.IntegerField(null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    cover_color = models.SmallIntegerField(default=1)  
    cover_url = models.URLField(max_length=500, blank=True)  
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_url = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title



class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_pages')
    page_number = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('book', 'page_number')  
        ordering = ['page_number']

    def __str__(self):
        return f"{self.book.title} - {self.page_number}-sahifa"



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')  
    def __str__(self):
        return f"{self.user} - {self.book}"



class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.IntegerField(default=1)
    total_pages = models.IntegerField()
    finished_at = models.DateTimeField(null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book} ({self.current_page}/{self.total_pages})"