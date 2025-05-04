from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import Q

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-date')
    
    @action(detail=False, methods=['get'])
    def non_vues(self, request):
        notifications = Notification.objects.filter(
            user=request.user,
            est_vue=False
        ).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def marquer_comme_lues(self, request):
        notifications = Notification.objects.filter(
            user=request.user,
            est_vue=False
        )
        notifications.update(est_vue=True)
        return Response({"status": "notifications marquées comme lues"}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def par_categorie(self, request):
        categorie = request.query_params.get('categorie', None)
        if categorie:
            notifications = Notification.objects.filter(
                user=request.user,
                categorie__id=categorie
            ).order_by('-date')
            serializer = self.get_serializer(notifications, many=True)
            return Response(serializer.data)
        return Response({"error": "Paramètre 'categorie' requis"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def objectifs(self, request):
        # Notifications liées aux objectifs - filtre selon vos critères spécifiques
        notifications = Notification.objects.filter(
            user=request.user,
            message__icontains="objectif"
        ).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def budgetaires(self, request):
        # Notifications budgétaires - filtre selon vos critères spécifiques
        notifications = Notification.objects.filter(
            user=request.user,
            message__icontains="budget"
        ).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def habitudes(self, request):
        # Notifications habitudes et tendances
        habitudes_keywords = ["augmenté", "diminué", "tendance", "récurrent", "généralement"]
        query = Q(user=request.user)
        for keyword in habitudes_keywords:
            query |= Q(message__icontains=keyword)
        notifications = Notification.objects.filter(query).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def conseils(self, request):
        # Notifications proactives et conseils
        conseils_keywords = ["Conseil", "Astuce", "Défi", "Essayez", "Pensez"]
        query = Q(user=request.user)
        for keyword in conseils_keywords:
            query |= Q(message__icontains=keyword)
        notifications = Notification.objects.filter(query).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        # Notifications statistiques
        stats_keywords = ["Résumé", "statistique", "pourcentage", "total", "meilleur"]
        query = Q(user=request.user)
        for keyword in stats_keywords:
            query |= Q(message__icontains=keyword)
        notifications = Notification.objects.filter(query).order_by('-date')
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)