# notification/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings
from authentification.models import User
from goals.models import Objectif


class Notification(models.Model):
    TYPES_NOTIFICATION = [
        ('JALON', 'Jalon atteint'),
        ('ECHEANCE', 'Proximité échéance'),
        ('RAPPEL', 'Rappel contribution'),
        ('SUGGESTION', 'Suggestion d\'amélioration'),
        ('BUDGET', 'Alerte budget')
    ]

    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,  # Allow null temporarily for migration
        default=None  # Set a default value
    )
    objectif = models.ForeignKey(
        Objectif,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=TYPES_NOTIFICATION,
        default='RAPPEL'
    )
    message = models.TextField(max_length=2000)
    date_creation = models.DateTimeField(default=timezone.now)
    est_vue = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.get_type_display()} - {self.message[:50]}"
