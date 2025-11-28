from django.shortcuts import render
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
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
    permission_classes = [AllowAny]

class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

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
