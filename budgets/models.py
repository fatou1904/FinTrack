from django.db import models
from authentification.models import User

class Budget(models.Model):
    MOIS_CHOICES = [
        ('janvier', 'Janvier'),
        ('fevrier', 'Février'),
        ('mars', 'Mars'),
        ('avril', 'Avril'),
        ('mai', 'Mai'),
        ('juin', 'Juin'),
        ('juillet', 'Juillet'),
        ('aout', 'Août'),
        ('septembre', 'Septembre'),
        ('octobre', 'Octobre'),
        ('novembre', 'Novembre'),
        ('decembre', 'Décembre'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    mois = models.CharField(max_length=15, choices=MOIS_CHOICES)                   
    annee = models.IntegerField()
    revenue = models.FloatField()
    budget_total = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mois}/{self.annee}"
