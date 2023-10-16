import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from reservation.models import ReservedDate

logger = logging.getLogger("reservation")


@receiver(pre_delete, sender=ReservedDate)
def prevent_deletion(sender, instance, **kwargs):
    raise Exception("Deletion is not allowed for model ReservedDate")
