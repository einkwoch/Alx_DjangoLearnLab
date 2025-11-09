from .models import Author,Book, Librarian, Library

Author_1 = Author.objects.create(name = 'Emmanuel Izu')
Author_2 = Author.objects.create(name = 'Kosi Nkwocha')
Author_3 = Author.objects.create(name = 'kamsi Nkwocha')

Book_1 = Book.objects.create(title = "Arrow of God", author = Author_1)
Book_2 = Book.objects.create(title = "Tech Gurus", author = Author_2)
Book_3 = Book.objects.create(title = "Introduction to python", author = Author_3)
Book_4 = Book.objects.create(title = "Introduction to Django", author = Author_1)
Book_5 = Book.objects.create(title = "Introduction to Javascript", author = Author_2)
Book_6 = Book.objects.create(title = "Introduction to Stanford", author = Author_3)

LibModel_1 = Library.objects.create(name = 'Standard Books')
LibModel_2 = Library.objects.create(name = 'Knowledge Books')

LibModel_1.add(Book_1, Book_2, Book_3)
LibModel_1.add(Book_4, Book_5, Book_6)

LibrModel_1 = Librarian.objects.create(name = 'Good', Library = LibModel_1)
LibrModel_2 = Librarian.objects.create(name = 'Very Good', Library = LibModel_2)

# Query all books by a specific author.
author_name='Emmanuel Izu'
author = Author.objects.get(name=author_name)
Book.objects.filter(author=author)



# List all books in a library.
library_name = 'Standard Books'
library = Library.objects.get(name=library_name)
library.books.all()

#Retrieve the librarian for a library.
libarian = LibrModel_1
print(libarian.name)