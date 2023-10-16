from django.db.models import TextChoices


class ReservationStatus(TextChoices):
    Pending = "Pending", "pending"
    Confirmed = "Confirmed", "confirmed"
    Canceled = "Canceled", "canceled"
