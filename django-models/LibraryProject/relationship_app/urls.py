from django.urls import path
from .views import list_books, LibraryDetailView, path, RegisterView, admin_view, librarian_view, member_view, edit_book,add_book,delete_book
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for the class-based view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # Using built-in login view
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # Using built-in logout view
    path('register/', RegisterView.as_view(), name='views.register'),  # Custom registration view
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('book/add/', add_book, name='add_book'),  # URL for adding a book
    path('book/edit/<int:book_id>/', edit_book, name='edit_book'),  # URL for editing a book
    path('book/delete/<int:book_id>/', delete_book, name='delete_book'),  # URL for deleting a book
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Existing library view
]