from datetime import timedelta, date

from core.models import AbstractBaseModel
from django.db import models
from django.conf import settings

from constants import ReservationStatus


class Reservation(AbstractBaseModel):
    listing = models.ForeignKey(
        "listing.Listing", on_delete=models.PROTECT, related_name="reservations"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reservations", on_delete=models.PROTECT
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    num_rooms = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ReservationStatus.choices,
        default=ReservationStatus.Pending,
    )

    def __str__(self):
        return "{}/{}".format(self.listing.name, self.customer.username)

    def save(self, *args, **kwargs):
        self.total_price = self.num_rooms * self.listing.price_per_room

        if self.pk is not None:
            # Check if the reservation status has changed from 'Canceled' to something else
            original_reservation = Reservation.objects.get(pk=self.pk)
            if original_reservation.status == ReservationStatus.Canceled and self.status != ReservationStatus.Canceled:
                raise Exception("You cannot change the status of a canceled reservation.")

        # Create or update ReservedDate instances for the reservation's date range in create sate
        if self._state.adding:
            self.change_reserved_rooms_number("create")

        super().save(*args, **kwargs)

    # Change ReservedDate instances func for the reservation's date range
    def change_reserved_rooms_number(self, level="create"):
        from reservation.models import ReservedDate
        current_date = self.start_date
        end_date = self.end_date
        if type(current_date) == str:
            current_date = date.fromisoformat(str(current_date))
        if type(end_date) == str:
            end_date = date.fromisoformat(str(end_date))
        while current_date < end_date:
            if level == "create":
                reserved_date, _ = ReservedDate.objects.get_or_create(
                    listing=self.listing, date=current_date
                )
                reserved_date.num_rooms_reserved += self.num_rooms
            else:
                reserved_date = ReservedDate.objects.get(
                    listing=self.listing, date=current_date
                )
                reserved_date.num_rooms_reserved -= self.num_rooms
            reserved_date.save()
            current_date += timedelta(days=1)
