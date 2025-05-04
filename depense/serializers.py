from rest_framework import serializers
from .models import Depense, Budget
from categories.serializers import CategorieSerializer

class DepenseSerializer(serializers.ModelSerializer):
    categorie_details = CategorieSerializer(source='categorie', read_only=True)
    
    class Meta:
        model = Depense
        fields = ['id', 'user', 'categorie', 'categorie_details', 'date', 'montant', 'description']
        
class BudgetSerializer(serializers.ModelSerializer):
    categorie_details = CategorieSerializer(source='categorie', read_only=True)
    
    class Meta:
        model = Budget
        fields = ['id', 'user', 'categorie', 'categorie_details', 'montant', 'mois', 'annee']