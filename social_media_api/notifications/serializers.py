from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()  # To represent actor in user-friendly format
    target = serializers.SerializerMethodField()  # To serialize the target object

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'target', 'timestamp']

    def get_target(self, obj):
        return {
            "id": obj.target_id,
            "type": str(obj.target_ct),  # This can give you the type of target object
        }