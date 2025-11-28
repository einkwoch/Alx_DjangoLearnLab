from django.urls import path
from . import views

urlpatterns = [
    path('authors/',views.AuthorListCreateAPIView.as_view()),
    path('books/',views.BookListCreateAPIView.as_view()),
    path('book/list/',views.ListView.as_view()),
    path('book/detail/<int:pk>/',views.DetailView.as_view()),
    path('books/create/',views.CreateView.as_view()),
    path('books/update/<int:pk>/',views.UpdateView.as_view()),
    path('books/delete/<int:pk>/',views.DeleteView.as_view()),
]