from django.urls import path, include
from .views import BookList,PersonList, BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books_all', BookViewSet, basename='book_all')


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('persons/', PersonList.as_view(), name='person-list'),
    path('', include(router.urls))   
]

