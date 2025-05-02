from django.db import models

from authentification.models import User
from categories.models import Categorie

# Create your models here.
class Objectif(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    pourcentage = models.FloatField()
    budget_mensuel = models.FloatField()
    class Meta:
        unique_together = ('user', 'categorie') #le unique together permet au user de ne pas avoir plusieurs objectifs pour une meme categorie
    def __str__(self):
        return f"{self.user.username} - {self.categorie.nom} ({self.pourcentage}%)"