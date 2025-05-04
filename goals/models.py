from django.db import models
from django.utils import timezone
from authentification.models import User
from decimal import Decimal

class Jalon(models.Model):
    objectif = models.ForeignKey('Objectif', on_delete=models.CASCADE, related_name='jalons')
    pourcentage = models.IntegerField()  # 25, 50, 75
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    atteint = models.BooleanField(default=False)
    date_atteinte = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Jalon {self.pourcentage}% pour {self.objectif.titre}"

class Objectif(models.Model):
    TYPES_OBJECTIF = [
        ('URGENCE', 'Fonds d\'urgence'),
        ('ACHAT', 'Achat important'),
        ('VACANCES', 'Vacances'),
        ('EDUCATION', 'Éducation'),
        ('RETRAITE', 'Retraite'),
        ('DETTE', 'Remboursement de dette'),
        ('AUTRE', 'Autre'),
    ]

    CHOIX_STATUT = [
        ('ACTIF', 'En cours'),
        ('TERMINE', 'Atteint'),
        ('PAUSE', 'En pause'),
        ('ABANDONNE', 'Abandonné'),
    ]

    FREQUENCE_CHOICES = [
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
        ('annuelle', 'Annuelle'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objectifs')
    titre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPES_OBJECTIF)

    montant_cible = models.DecimalField(max_digits=12, decimal_places=2)
    montant_actuel = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    date_debut = models.DateField(default=timezone.now)
    date_echeance = models.DateField()

    statut = models.CharField(max_length=20, choices=CHOIX_STATUT, default='ACTIF')

    contribution_automatique = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    frequence_contribution = models.CharField(
        max_length=20,
        choices=FREQUENCE_CHOICES,
        default='mensuelle'
    )

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_realisation = models.DateTimeField(null=True, blank=True)
    est_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_creation']

    @property
    def pourcentage_progression(self):
        if self.montant_cible == 0:
            return Decimal('0')
        return min(Decimal('100'), (self.montant_actuel * Decimal('100') / self.montant_cible))

    @property
    def montant_restant(self):
        return max(Decimal('0'), self.montant_cible - self.montant_actuel)

    @property
    def jours_restants(self):
        if self.statut == 'TERMINE':
            return 0
        aujourdhui = timezone.now().date()
        return max(0, (self.date_echeance - aujourdhui).days)

    @property
    def rythme_actuel(self):
        if not self.contributions.exists():
            return Decimal('0')
        premiere_contribution = self.contributions.order_by('date').first()
        jours_ecoules = (timezone.now().date() - premiere_contribution.date).days
        if jours_ecoules == 0:
            return Decimal('0')
        total_contributions = self.contributions.aggregate(total=models.Sum('montant'))['total']
        return Decimal(str(total_contributions)) / Decimal(str(jours_ecoules))

    @property
    def estimation_completion(self):
        if self.rythme_actuel == 0:
            return None
        montant_restant = self.montant_restant
        jours_necessaires = int(montant_restant / self.rythme_actuel)
        return timezone.now().date() + timezone.timedelta(days=jours_necessaires)

    def verifier_jalons(self):
        progression = self.pourcentage_progression
        for jalon in self.jalons.filter(atteint=False):
            if progression >= jalon.pourcentage:
                jalon.atteint = True
                jalon.date_atteinte = timezone.now()
                jalon.save()

    def __str__(self):
        return f"{self.titre} - {self.utilisateur.username}"

class Contribution(models.Model):
    objectif = models.ForeignKey(Objectif, on_delete=models.CASCADE, related_name='contributions')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.CharField(max_length=200, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.montant} pour {self.objectif.titre} le {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.objectif.verifier_jalons()
