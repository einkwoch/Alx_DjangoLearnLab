>>> B1 = Book.objects.all()
>>> B1 = Book.objects.get(pk=1)
>>> B1.delete()
(1, {'bookshelf.Book': 1})
>>> Book.objects.all()
<QuerySet []>