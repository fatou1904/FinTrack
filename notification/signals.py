from django.db.models.signals import post_save
from django.dispatch import receiver
from goals.models import Objectif, Jalon
from .models import Notification

@receiver(post_save, sender=Objectif)
def creer_notifications_objectif(sender, instance, created, **kwargs):
    if not created:
        # Vérifier l'échéance
        jours_restants = instance.jours_restants
        if jours_restants in [30, 15, 7, 3, 1]:
            Notification.objects.create(
                utilisateur=instance.utilisateur,
                objectif=instance,
                type='ECHEANCE',
                message=f"Plus que {jours_restants} jour{'s' if jours_restants > 1 else ''} pour atteindre votre objectif '{instance.titre}'"
            )

@receiver(post_save, sender=Jalon)
def creer_notification_jalon(sender, instance, created, **kwargs):
    if instance.atteint:
        Notification.objects.create(
            utilisateur=instance.objectif.utilisateur,
            objectif=instance.objectif,
            type='JALON',
            message=f"Félicitations ! Vous avez atteint {instance.pourcentage}% de votre objectif '{instance.objectif.titre}'"
        )
