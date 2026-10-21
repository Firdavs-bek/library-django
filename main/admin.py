from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Genre, Book, BookPage, Favorite, ReadingProgress


class BookPageInline(admin.StackedInline):
 
    model = BookPage
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'rating', 'pages', 'created_at')
    list_filter = ('genre',)
    search_fields = ('title', 'author')
    inlines = [BookPageInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user  
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        book = form.instance             
        book.pages = book.book_pages.count()
        book.save(update_fields=['pages'])


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Rol', {'fields': ('role',)}),)
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(Favorite)
admin.site.register(ReadingProgress)
