from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from .models import Objectif, Contribution
from .serializers import ObjectifSerializer, ContributionSerializer


class ObjectifViewSet(viewsets.ModelViewSet):
    serializer_class = ObjectifSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Objectif.objects.filter(utilisateur=self.request.user)
        type_objectif = self.request.query_params.get('type', None)
        statut = self.request.query_params.get('statut', None)

        if type_objectif:
            queryset = queryset.filter(type=type_objectif)
        if statut:
            queryset = queryset.filter(statut=statut)

        return queryset

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

    def list_contributions(self, request, pk=None):
        objectif = self.get_object()
        contributions = objectif.contributions.all().order_by('-date')
        serializer = ContributionSerializer(contributions, many=True)
        return Response(serializer.data)

    def get_stats(self, request):
        objectifs = self.get_queryset()
        stats = {
            'total_objectifs': objectifs.count(),
            'objectifs_actifs': objectifs.filter(statut='ACTIF').count(),
            'objectifs_termines': objectifs.filter(statut='TERMINE').count(),
            'montant_total_epargne': objectifs.aggregate(total=Sum('montant_actuel'))['total'] or 0,
            'progression_moyenne': objectifs.filter(montant_cible__gt=0).aggregate(
                avg=Avg('montant_actuel') * 100 / Avg('montant_cible')
            )['avg'] or 0,
            'repartition_types': {
                type_obj: objectifs.filter(type=type_obj).count()
                for type_obj, _ in Objectif.TYPES_OBJECTIF
            }
        }
        return Response(stats)

    @action(detail=True, methods=['post'])
    def marquer_complete(self, request, pk=None):
        objectif = self.get_object()
        objectif.est_complete = True
        objectif.statut = 'TERMINE'
        objectif.date_realisation = timezone.now()
        objectif.save()
        return Response(
            {'status': 'Objectif marqué comme complété'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def ajouter_contribution(self, request, pk=None):
        objectif = self.get_object()
        serializer = ContributionSerializer(data=request.data)

        if serializer.is_valid():
            contribution = serializer.save(objectif=objectif)
            objectif.montant_actuel += contribution.montant

            if objectif.montant_actuel >= objectif.montant_cible:
                objectif.est_complete = True
                objectif.statut = 'TERMINE'
                objectif.date_realisation = timezone.now()

            objectif.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def objectifs_actifs(self, request):
        objectifs = self.get_queryset().filter(
            statut='ACTIF',
            date_echeance__gte=timezone.now().date()
        )
        serializer = self.get_serializer(objectifs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def objectifs_completes(self, request):
        objectifs = self.get_queryset().filter(statut='TERMINE')
        serializer = self.get_serializer(objectifs, many=True)
        return Response(serializer.data)
