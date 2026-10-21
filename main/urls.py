from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.books, name='books'),
    path('books/<int:pk>/', views.book_detail, name='book'),
    path('books/<int:pk>/read/', views.read, name='read'),
    path('login/', views.auth_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
