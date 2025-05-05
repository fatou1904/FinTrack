from rest_framework import serializers

from notification.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'message', 'montant_depense', 'seuil_objectif', 'categorie', 'date']