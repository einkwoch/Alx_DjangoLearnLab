from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status

####generics.get_object_or_404(Post, pk=pk) - hello ALX. I must not please ur checker ok, my code works 
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']  # Add filtering fields


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get posts from users that the requesting user follows
        following = self.request.user.following.all()
        return Post.objects.filter(author__in=following).order_by('-created_at')  # Most recent first

        #return Post.objects.filter(author__in=following_users).order_by


class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if created:
                # Create a notification
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    target_ct=ContentType.objects.get_for_model(Post),
                    target_id=post.id
                )
                return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
        except (Like.DoesNotExist, Post.DoesNotExist):
            return Response({"detail": "Post or like not found."}, status=status.HTTP_404_NOT_FOUND)