from datetime import date

from django.db.models import Q, Max
from django.db import models
from django.conf import settings

from core.models import AbstractBaseModel


class Listing(AbstractBaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="listings", on_delete=models.PROTECT
    )

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    total_rooms = models.PositiveIntegerField()
    price_per_room = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField(blank=True, null=True)
    amenities = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["owner", "name"]

    def __str__(self):
        return "{}|{}".format(self.pk, self.name)

    def is_available(self, num_rooms_required, start_date, end_date):
        if type(start_date) == str:
            start_date = date.fromisoformat(start_date)
        if type(end_date) == str:
            end_date = date.fromisoformat(end_date)

        availability_rooms_list = list(
            self.reserved_dates.filter(Q(date__gte=start_date) & Q(date__lt=end_date))
            .annotate(
                available_rooms=self.total_rooms
                - Max("num_rooms_reserved")
                - num_rooms_required
            )
            .values_list("available_rooms", flat=True)
        )

        dates_are_available = all(value >= 0 for value in availability_rooms_list)

        if not dates_are_available:
            return False, "Rooms are fully booked from date {} to date {}".format(
                start_date, end_date
            )
        return True, ""
