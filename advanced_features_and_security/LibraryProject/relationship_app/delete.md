>>> from bookshelf.models import Book 
>>> book = Book.objects.all()
>>> book = Book.objects.get(pk=1)
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>