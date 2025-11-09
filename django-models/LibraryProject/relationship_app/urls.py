from django.urls import path
from .views import list_books, LibraryDetailView, path, RegisterView, login_view, logout_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Using built-in logout view
    path('register/', RegisterView.as_view(), name='register'),
]