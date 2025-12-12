from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(User, related_name='actor', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)  # E.g., "liked your post"
    target_ct = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_ct', 'target_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"
