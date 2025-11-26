from django.contrib import admin
from .models import Author, Book
# Register your models here.


class Book_Cus_D(admin.ModelAdmin):
    list_display = ('title','publication_year','author')


class Author_Cus_D(admin.ModelAdmin):
    list_display = ('name',)
   
    
admin.site.register(Book,Book_Cus_D)
admin.site.register(Author,Author_Cus_D)