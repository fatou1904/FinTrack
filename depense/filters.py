import django_filters
from .models import Depense
from django.db.models import Q

class DepenseFilter(django_filters.FilterSet):
    montant_min = django_filters.NumberFilter(field_name='montant', lookup_expr='gte')
    montant_max = django_filters.NumberFilter(field_name='montant', lookup_expr='lte')
    date_debut = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_fin = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    class Meta:
        model = Depense
        fields = ['categorie', 'montant_min', 'montant_max', 'date_debut', 'date_fin'] 
