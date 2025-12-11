from django.urls import path

from .views import RegisterView, LoginView, UserProfileView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),  # Need to implement UserProfileView
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),  # New endpoint
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),  
]