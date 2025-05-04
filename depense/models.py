from django.db import models
from authentification.models import User
from categories.models import Categorie

class Depense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    montant = models.FloatField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.categorie} - {self.montant} - {self.date.strftime('%d/%m/%Y')}"
    
    class Meta:
        ordering = ['-date']

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    montant = models.FloatField()
    mois = models.IntegerField()
    annee = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'categorie', 'mois', 'annee')