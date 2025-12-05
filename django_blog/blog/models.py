from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Establish relationship with Post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Author of the comment
    content = models.TextField()  # The text of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # When the comment was created
    updated_at = models.DateTimeField(auto_now=True)  # When the comment was last updated

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'