from django.urls import path
from . import views 

urlpatterns = [
    path('posts/', views.ListBlogPost.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.DetailBlogPost.as_view(), name = 'detail'),
    path('posts/new/', views.CreatBlogPost.as_view(), name = 'create'),
    path('posts/<int:pk>/edit/', views.UpdateBlogPost.as_view(), name = 'update'),
    path('posts/<int:pk>/delete/', views.DeleteBlogPost.as_view(), name = 'delete'),
]