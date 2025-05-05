from django.db import models

from authentification.models import User
from categories.models import Categorie

# Create your models here.

class Depense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    montant = models.FloatField(),
    description = models.TextField(blank=True, null=True)