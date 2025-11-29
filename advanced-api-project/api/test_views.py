# api/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book,Author

class BookAPITests(APITestCase):
    
    def setUp(self):
        # Create an author instance to use in tests
        self.author = Author.objects.create(name='Test Author')  # Create an Author instance

        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author
        }
        self.book = Book.objects.create(**self.book_data)

    def test_create_book(self):
        # Authenticate user
        self.client.login(username='testuser', password='testpass')
        
        response = self.client.post(
            reverse('book-create'),  # or the correct URL name for creating a book
            {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Ensure one more book is created
        self.assertEqual(Book.objects.get(pk=2).title, 'New Book')  # Adjust ID if needed

    def test_list_books(self):
        response = self.client.get(reverse('book-list'))  # Replace with the correct URL name
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book is initially created

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.put(
            reverse('book-update', args=[self.book.id]),  # Ensure this URL matches your update URL
            {'title': 'Updated Book Title', 'publication_year': 2024, 'author': 1},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book Title')

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(reverse('book-delete', args=[self.book.id]))  # Adjust URL pattern
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)  # Should be 0 after deletion

    def test_search_books(self):
        response = self.client.get(reverse('book-list') + '?search=Test Book')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should find exactly 1 book

    def test_permissions(self):
        # Test unauthenticated access to create a book
        response = self.client.post(reverse('book-create'),  # Ensure this URL matches your update URL
            {'title': 'TestU Book Title', 'publication_year': 2024, 'author': 1},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should be forbidden

        # Test authenticated access
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('book-create'),  # Ensure this URL matches your update URL
            {'title': 'TestA Book Title', 'publication_year': 2024, 'author': 1},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Should be allowed