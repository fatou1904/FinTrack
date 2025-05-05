from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from depense.models import Depense
from depense.serializer import DepenseSerializer
from goals.models import Objectif
from notification.models import Notification
from django.db.models import Sum

class DepenseList(generics.ListCreateAPIView):
    queryset = Depense.objects.all()
    serializer_class = DepenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Depense.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        depense = serializer.save(user=request.user)

        objectif = Objectif.objects.filter(
            user=depense.user, 
            categorie=depense.categorie
        ).first()

        if objectif:
            # Calculer la somme des dépenses pour la catégorie
            total_depense = Depense.objects.filter(
                user=depense.user, 
                categorie=depense.categorie
            ).aggregate(Sum('montant'))['montant__sum'] or 0

            # Calculer le pourcentage des dépenses par rapport à l'objectif mensuel
            pourcentage_depense = (total_depense / objectif.budget_mensuel) * 100

            # Vérifier si le pourcentage dépasse le seuil
            if pourcentage_depense > objectif.pourcentage:
                message = f"Vous avez dépassé votre objectif de {objectif.pourcentage}% pour la catégorie '{depense.categorie}'. Vous êtes à {pourcentage_depense:.2f}%."
                Notification.objects.create(
                    user=depense.user,
                    message=message,
                    categorie=depense.categorie,
                    montant_depense=total_depense,
                    seuil_objectif=objectif.pourcentage,
                    est_vue=False
                )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
