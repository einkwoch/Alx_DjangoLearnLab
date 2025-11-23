from django.contrib import admin
from .models import Book, Person

# Register your models here.
class Book_Cus_D(admin.ModelAdmin):
    list_display = ('title','author')


class Person_Cus_D(admin.ModelAdmin):
    list_display = ('title','first_name','last_name','occupation',)
   
    
admin.site.register(Book,Book_Cus_D)
admin.site.register(Person,Person_Cus_D)