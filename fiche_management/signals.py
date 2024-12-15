from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import notify
from .models import Sheet

class SheetSignalHandler:
    """
    Classe gérant les signaux liés au modèle Sheet.
    """
    @staticmethod
    @receiver(post_save, sender=Sheet)
    def notify_on_validation(sender, instance, created, **kwargs):
        """
        Notification envoyée lorsque la fiche est validée ou rejetée.
        """
        if not created:  # Vérifie que ce n'est pas une nouvelle fiche
            if instance.is_validated is True:  # Si la fiche est validée
                notify.send(
                    sender=instance,
                    recipient=instance.enseignant,
                    verb="Votre fiche a été validée.",
                    description=f"La fiche pour {instance.promotion} a été validée."
                )
            elif instance.is_validated is False:  # Si la fiche est rejetée
                notify.send(
                    sender=instance,
                    recipient=instance.enseignant,
                    verb="Votre fiche a été rejetée.",
                    description=f"Motif : {instance.motif_de_rejet}"
                )

    @staticmethod
    @receiver(post_delete, sender=Sheet)
    def notify_on_delete(sender, instance, **kwargs):
        """
        Notification envoyée lorsque la fiche est supprimée.
        """
        notify.send(
            sender=instance,
            recipient=instance.enseignant,
            verb="Votre fiche a été supprimée.",
            description=f"La fiche pour {instance.promotion} a été supprimée."
        )
