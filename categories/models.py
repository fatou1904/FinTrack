from django.db import models

# Create your models here.
class Categorie(models.Model):
    CATEGORY_DEPENSE = [
        ('alimentaire', 'Alimentaire'),
        ('location', 'Location'),
        ('voiture', 'Voiture'),
        ('divertissement', 'Divertissement'),
        ('transport', 'Transport'),
        ('facture', 'Facture'),
        ('famille', 'Famille'),
        ('hopital', 'Hopital')
    ]
    Nomcategorie = models.CharField(max_length=100, choices=CATEGORY_DEPENSE, unique=True)
    
    def __str__(self):
        return self.Nomcategorie