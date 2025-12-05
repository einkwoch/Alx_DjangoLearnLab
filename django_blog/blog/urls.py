from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('posts/', views.ListBlogPost.as_view(), name = 'posts'),
    path('posts/<int:pk>/', views.DetailBlogPost.as_view(), name = 'detail'),
    path('post/new/', views.CreatBlogPost.as_view(), name = 'create'),
    path('post/<int:pk>/update/', views.UpdateBlogPost.as_view(), name = 'update'),
    path('post/<int:pk>/delete/', views.DeleteBlogPost.as_view(), name = 'delete'),
    path('register/', views.RegisterView, name = 'register'),
    path('login/', LoginView.as_view(), name='login'),         # Built-in login view
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),  # For creating a new comment
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_edit'),  # For editing a comment
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),  # For deleting a comment
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='create_post'),
    path('search/', views.search_view, name='post_search'),  # Search functionality 
]