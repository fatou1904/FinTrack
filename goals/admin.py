from django.contrib import admin
from .models import Objectif, Contribution, Jalon

class JalonInline(admin.TabularInline):
    model = Jalon
    extra = 0

class ContributionInline(admin.TabularInline):
    model = Contribution
    extra = 0

@admin.register(Objectif)
class ObjectifAdmin(admin.ModelAdmin):
    list_display = ('titre', 'utilisateur', 'type', 'montant_cible',
                   'montant_actuel', 'date_echeance', 'statut')
    list_filter = ('statut', 'type', 'frequence_contribution')
    search_fields = ('titre', 'utilisateur__username', 'description')
    date_hierarchy = 'date_creation'
    inlines = [JalonInline, ContributionInline]

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    list_display = ('objectif', 'montant', 'date', 'note')
    list_filter = ('date', 'objectif__type')
    search_fields = ('objectif__titre', 'note')
    date_hierarchy = 'date'

@admin.register(Jalon)
class JalonAdmin(admin.ModelAdmin):
    list_display = ('objectif', 'pourcentage', 'montant', 'atteint', 'date_atteinte')
    list_filter = ('atteint', 'pourcentage')
    search_fields = ('objectif__titre',)
