from django.urls import path
from . import views

urlpatterns = [
    path('authors/',views.AuthorListCreateAPIView.as_view()),
    path('books/',views.BookListCreateAPIView.as_view()),
]