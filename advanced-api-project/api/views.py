from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.prefetch_related('books')
    serializer_class = AuthorSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

#### IMPLEMENTING GENERIC VIEWS TO HANDLE CRUD OPERATIONS
class ListView(generics.ListAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('title', 'author', 'publication_year')
    search_fields = ['title', 'author__name']  # Added author__name
    ordering_fields = ['author', 'publication_year']

class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
