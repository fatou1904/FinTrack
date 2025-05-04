from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'message', 'date_creation', 'est_vue', 'objectif']
        read_only_fields = ['id', 'date_creation']
