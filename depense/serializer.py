from rest_framework import serializers

from depense.models import Depense

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = ['categorie', 'montant']
    
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError("Le montant doit être supérieur à zéro.")
        return value

        
    def create(self, validated_data):
        depense = Depense.objects.create(**validated_data)
        return depense