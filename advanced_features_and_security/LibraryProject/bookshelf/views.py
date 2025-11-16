from django.shortcuts import render
from .models import Book, Author
from django.views.generic.detail import DetailView
from .models import Library, UserProfile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required
from .forms import ExampleForm, SearchForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

# Create your views here.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """Function-based view to list all books."""
    form = SearchForm(request.GET or None)
    books = Book.objects.select_related("author").all()
    if form.is_valid():
        q = form.cleaned_data.get("q")
    if q:
        # Safe parameterized filtering via ORM
        books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        return render(request, 'bookshelf/list_books.html', {'books': books, 'search_form': form})

class LibraryDetailView(DetailView):
    """Class-based view to display details of a specific library."""
    model = Library
    template_name = 'bookshelf/library_detail.html'  # Specify your template for display
    context_object_name = 'library'


# User Registration View
class RegisterView(CreateView):
    form_class = UserCreationForm()
    template_name = 'bookshelf/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Automatically log the user in after registration
        return super().form_valid(form)

# Optional: If creating function-based views for Login and Logout
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('profile')
    else:
        form = AuthenticationForm(request)
        return render(request, 'bookshelf/login.html', {'form': form})


def logout_view(request):
    # Assuming you have set up logout logic
    logout(request)
    return render(request, 'bookshelf/logout.html')

def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'bookshelf/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'bookshelf/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'bookshelf/member_view.html')

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])
def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    else:
        form = ExampleForm()
        return render(request, 'bookshelf/add_book.html', {'form': form})

# View to edit a book
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    else:
        form = ExampleForm(instance=book)
        return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

# View to delete a book
@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["GET", "POST"])
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})