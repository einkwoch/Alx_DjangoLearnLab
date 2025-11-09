from django.urls import path
from .views import list_books, LibraryDetailView, path, RegisterView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('books/', list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # URL for the class-based view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # Using built-in login view
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # Using built-in logout view
    path('register/', RegisterView.as_view(), name='register'),  # Custom registration view
]