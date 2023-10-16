import logging

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from constants import ReservationStatus
from reservation.models import Reservation

logger = logging.getLogger("reservation")


@receiver(pre_delete, sender=Reservation)
def prevent_deletion(sender, instance, **kwargs):
    raise PermissionError("Deletion is not allowed for model Reservation")


@receiver(pre_save, sender=Reservation)
def status_reduce_reserved_rooms_number(sender, instance, **kwargs):
    if instance.id is None:
        return
    try:
        original_reservation = Reservation.objects.get(id=instance.id)
        if (
            original_reservation.status != instance.status
            and instance.status == ReservationStatus.Canceled
        ):
            instance.change_reserved_rooms_number(level="delete")
    except Exception as e:
        logger.error(msg=e)
