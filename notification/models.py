from django.db import models

from authentification.models import User
from categories.models import Categorie

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=2000)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    montant_depense = models.FloatField()
    seuil_objectif = models.FloatField()
    date = models.DateField(auto_now_add=True)
    est_vue = models.BooleanField(default=False)
    
    def __str__(self):
        return self.message