from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Depense, Budget
from .serializers import DepenseSerializer, BudgetSerializer
from .filters import DepenseFilter
from datetime import datetime

class DepenseViewSet(viewsets.ModelViewSet):
    serializer_class = DepenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DepenseFilter
    search_fields = ['description']
    ordering_fields = ['date', 'montant', 'categorie']
    
    def get_queryset(self):
        return Depense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    @action(detail=False, methods=['get'])
    def historique_mensuel(self, request):
        annee = request.query_params.get('annee', datetime.now().year)
        
        historique = Depense.objects.filter(
            user=request.user,
            date__year=annee
        ).annotate(
            mois=TruncMonth('date')
        ).values(
            'mois'
        ).annotate(
            total=Sum('montant')
        ).order_by('mois')
        
        return Response(historique)
    
    @action(detail=False, methods=['get'])
    def statistiques_categories(self, request):
        mois = request.query_params.get('mois', datetime.now().month)
        annee = request.query_params.get('annee', datetime.now().year)
        
        stats = Depense.objects.filter(
            user=request.user,
            date__month=mois,
            date__year=annee
        ).values(
            'categorie__nom'
        ).annotate(
            total=Sum('montant')
        ).order_by('-total')
        
        # Ajout de la comparaison avec le budget si défini
        for stat in stats:
            budget = Budget.objects.filter(
                user=request.user,
                categorie__nom=stat['categorie__nom'],
                mois=mois,
                annee=annee
            ).first()
            
            stat['budget'] = budget.montant if budget else 0
            stat['pourcentage'] = (stat['total'] / stat['budget'] * 100) if stat['budget'] else None
        
        return Response(stats)    

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categorie', 'mois', 'annee']
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)