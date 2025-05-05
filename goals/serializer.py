from rest_framework import serializers

from goals.models import Objectif

class GoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objectif
        fields = ['categorie', 'pourcentage', 'budget_mensuel']