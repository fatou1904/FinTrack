from rest_framework import serializers

from budgets.models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['mois', 'annee', 'revenue', 'budget_total']
        read_only_fields = ['date_creation']  # si je ne veux pas que l'utilisateur l'envoie manuellement
        
    def create(self, validated_data):
        return Budget.objects.create(**validated_data)