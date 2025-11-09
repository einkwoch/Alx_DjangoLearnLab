from django.shortcuts import render
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
# Create your views here.



def list_books(request):
    """Function-based view to list all books."""
    books = Book.objects.all()  # Query all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library."""
    model = Library
    template_name = 'library_detail.html'  # Specify your template for display
    context_object_name = 'library'