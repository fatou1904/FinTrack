from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'categorie', 'montant_depense', 'seuil_objectif', 'date', 'est_vue'] 
