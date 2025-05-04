from rest_framework import serializers
from .models import Objectif, Contribution, Jalon

class JalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jalon
        fields = ['id', 'pourcentage', 'montant', 'atteint', 'date_atteinte']
        read_only_fields = ['id', 'date_atteinte']

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['id', 'montant', 'date', 'note', 'date_creation']
        read_only_fields = ['id', 'date_creation']

class ObjectifSerializer(serializers.ModelSerializer):
    progression = serializers.SerializerMethodField()
    contributions = ContributionSerializer(many=True, read_only=True)
    jalons = JalonSerializer(many=True, read_only=True)
    jours_restants = serializers.SerializerMethodField()
    montant_restant = serializers.SerializerMethodField()
    rythme_actuel = serializers.SerializerMethodField()
    estimation_completion = serializers.SerializerMethodField()

    class Meta:
        model = Objectif
        fields = [
            'id', 'titre', 'description', 'type', 'montant_cible',
            'montant_actuel', 'date_debut', 'date_echeance',
            'statut', 'contribution_automatique', 'frequence_contribution',
            'date_creation', 'date_modification', 'date_realisation',
            'est_complete', 'progression', 'contributions', 'jalons',
            'jours_restants', 'montant_restant', 'rythme_actuel',
            'estimation_completion'
        ]
        read_only_fields = [
            'id', 'date_creation', 'date_modification',
            'progression', 'jours_restants', 'montant_restant',
            'rythme_actuel', 'estimation_completion'
        ]

    def get_progression(self, obj):
        return obj.pourcentage_progression

    def get_jours_restants(self, obj):
        return obj.jours_restants

    def get_montant_restant(self, obj):
        return float(obj.montant_restant)

    def get_rythme_actuel(self, obj):
        return float(obj.rythme_actuel)

    def get_estimation_completion(self, obj):
        estimation = obj.estimation_completion
        return estimation.isoformat() if estimation else None

    def validate_montant_actuel(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Le montant actuel ne peut pas être négatif."
            )
        return value

    def validate_montant_cible(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Le montant cible doit être supérieur à zéro."
            )
        return value
