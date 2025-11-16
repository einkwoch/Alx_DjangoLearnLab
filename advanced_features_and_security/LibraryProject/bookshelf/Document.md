Overview:

This app defines custom model-level permissions: can_view, can_create, can_edit, can_delete on the Book model.
These permissions are enforced in views via @permission_required.
Setup:

Ensure the app “bookshelf” is in INSTALLED_APPS and that django.contrib.auth and django.contrib.contenttypes are also installed.
Run:
python manage.py makemigrations
python manage.py migrate This creates Permission entries for the custom permissions.
Groups:

In Django Admin, create groups such as Viewers, Editors, Admins.
Assign permissions:
Viewers: can_view
Editors: can_view, can_create, can_edit
Admins: can_view, can_create, can_edit, can_delete (and optionally all built-in perms)
Add users to the appropriate groups.
Testing:

Create test users and assign them to the groups.
Log in and attempt to visit:
list_books view: require can_view
add_book view: requires can_create
edit_book view: requires can_edit
delete_book view: requires can_delete
Confirm access is allowed/denied as expected.


### SECURITY PRACTICE

Create forms.py (input validation and safer handling) Create an app-level forms.py (in the same app as your models and views) with validated forms for books and search.
forms.py:
from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
# strip=True trims whitespace; Django auto-escapes output in templates
title = forms.CharField(max_length=100, strip=True)
author = forms.ModelChoiceField(queryset=Author.objects.all())

ruby
Copy code
class Meta:
    model = Book
    fields = ["title", "author"]

def clean_title(self):
    title = self.cleaned_data["title"].strip()
    # Optional: basic check against only-whitespace
    if not title:
        raise forms.ValidationError("Title cannot be empty or whitespace.")
    return title
class SearchForm(forms.Form):
q = forms.CharField(max_length=100, required=False, strip=True)

Update your views to use forms (prevents injection and unsafe input) Replace raw request.POST handling with validated forms. Also use AuthenticationForm for login to validate credentials safely.
views.py (only the updated parts shown):
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
from django.db.models import Q

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
"""List books with optional safe search via SearchForm."""
form = SearchForm(request.GET or None)
books = Book.objects.select_related("author").all()
if form.is_valid():
q = form.cleaned_data.get("q")
if q:
# Safe parameterized filtering via ORM
books = books.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
return render(request, 'bookshelf/list_books.html', {'books': books, 'search_form': form})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(["GET", "POST"])
def add_book(request):
if request.method == 'POST':
form = BookForm(request.POST)
if form.is_valid():
form.save()
return redirect('list_books')
else:
form = BookForm()
return render(request, 'bookshelf/add_book.html', {'form': form})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@require_http_methods(["GET", "POST"])
def edit_book(request, book_id):
book = get_object_or_404(Book, id=book_id)
if request.method == 'POST':
form = BookForm(request.POST, instance=book)
if form.is_valid():
form.save()
return redirect('list_books')
else:
form = BookForm(instance=book)
return render(request, 'bookshelf/edit_book.html', {'form': form, 'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@require_http_methods(["GET", "POST"])
def delete_book(request, book_id):
book = get_object_or_404(Book, id=book_id)
if request.method == 'POST':
book.delete()
return redirect('list_books')
return render(request, 'bookshelf/delete_book.html', {'book': book})

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

Notes:

Using ModelForm and AuthenticationForm ensures safe, validated input and relies on Django’s built-in protections.
The ORM queries above are parameterized, which avoids SQL injection.
Template updates (CSRF, safer form rendering) Your templates already include {% csrf_token %}. Switch add/edit templates to use the form object instead of manual inputs. This reduces errors and leverages Django’s built-in escaping.
add_book.html (replace the form body):

<form method="post"> {% csrf_token %} {{ form.as_p }} <button type="submit">Add Book</button> </form>
edit_book.html (replace inputs):

<form method="post"> {% csrf_token %} {{ form.as_p }} <button type="submit">Update Book</button> </form>
Optional: In list_books.html, add a safe search form if you want search:

<form method="get"> {{ search_form.as_p }} <button type="submit">Search</button> </form>
Django auto-escapes variables in templates by default. Avoid using the |safe filter unless you know the content is trusted.

Secure settings (production hardening) Enable Django’s SecurityMiddleware and set secure headers and cookie flags. Only enable HTTPS-related settings in production when you have HTTPS enabled.
settings.py (production):
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]  # set appropriately

MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
# If you use django-csp, add its middleware just after SecurityMiddleware
# "csp.middleware.CSPMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

Browser-side protections
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

Note: SECURE_BROWSER_XSS_FILTER is deprecated in modern Django/browsers.
If your assignment requires it:
SECURE_BROWSER_XSS_FILTER = True # Older Django; newer browsers ignore X-XSS-Protection
CSRF and session cookie security (enable only under HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

Additional cookie hardening
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

Redirect all HTTP to HTTPS (production only)
SECURE_SSL_REDIRECT = True

HSTS (production only)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

If behind a proxy/HTTPS offloading, configure:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
If your app runs on a specific domain, set trusted origins for CSRF:
CSRF_TRUSTED_ORIGINS = ["https://yourdomain.com"]
Content Security Policy (CSP) Option A: Use django-csp (recommended).
Install: pip install django-csp
Add to MIDDLEWARE (after SecurityMiddleware): "csp.middleware.CSPMiddleware"
Configure directives:
settings.py (CSP):
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # inline styles only if necessary
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # prevents embedding

Adjust to allow any external CDNs you use (e.g., add "https://cdn.example.com" to SCRIPT_SRC/STYLE_SRC).

Option B: Manual middleware (if you can’t add django-csp).
Create a small middleware that sets the CSP header:

security.py (middleware file in your app):
class SetCSPHeaderMiddleware:
def init(self, get_response):
self.get_response = get_response
def call(self, request):
response = self.get_response(request)
response["Content-Security-Policy"] = (
"default-src 'self'; "
"script-src 'self'; "
"style-src 'self' 'unsafe-inline'; "
"img-src 'self' data:; "
"font-src 'self' data:; "
"connect-src 'self'; "
"frame-ancestors 'none'"
)
return response

Add "yourapp.security.SetCSPHeaderMiddleware" to MIDDLEWARE after SecurityMiddleware.

Documentation (inline comments)
In settings.py, add comments explaining each security setting and noting “enable under HTTPS only”.
In views, comment that ModelForm and AuthenticationForm provide validation and protection.
In templates, keep a short comment reminding to keep {% csrf_token %} in all POST forms.
Testing approach (manual checks)
CSRF: Remove {% csrf_token %} temporarily in a local branch and confirm Django blocks the POST with 403, then put it back.
XSS: Try entering <script>alert(1)</script> as a book title and confirm it renders escaped in templates (should show the tags as text, not execute).
SQL injection: Try search input like "' OR 1=1 --" and confirm results are not blown open; only normal matches should be returned.
CSP: Open the browser DevTools → Console, try to inject inline scripts or load scripts from disallowed domains and confirm CSP blocks them.
Cookies: Check the Set-Cookie headers in the network tab; verify Secure and HttpOnly flags are present in production.
Small fixes you may want to apply

Your model str methods should return strings, not tuples. For example:
def str(self):
return f"{self.title} by {self.author.name}"
Do similar for Library and Librarian to avoid admin/template issues.

Consider using settings.AUTH_USER_MODEL consistently. If you configured CustomUser as AUTH_USER_MODEL, the post_save signals bound to django.contrib.auth.models.User won’t fire. Bind signals to settings.AUTH_USER_MODEL instead.

Summary

Added forms.py with BookForm and SearchForm to centralize and validate input.
Updated views to use forms, ensuring parameterized ORM queries and CSRF protection.
Hardened settings with secure headers, cookie flags, and SecurityMiddleware.
Implemented CSP via django-csp or manual middleware.
Provided documentation and testing steps.
If you share your settings.py and list_books.html, I can tailor the CSP and search form to your exact static/CDN usage and template structure.






