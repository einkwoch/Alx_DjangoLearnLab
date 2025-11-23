from django.urls import path
from .views import BookList,PersonList

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('persons/', PersonList.as_view(), name='person-list'),
    
]
