from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics

# Create your views here.

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.prefetch_related('books')
    serializer_class = AuthorSerializer


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer