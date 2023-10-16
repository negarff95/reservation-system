from core.models import AbstractBaseModel
from django.db import models


class ReservedDate(AbstractBaseModel):
    listing = models.ForeignKey("listing.Listing", on_delete=models.PROTECT, related_name="reserved_dates")
    date = models.DateField()
    num_rooms_reserved = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.listing.name}|{self.date}"

    class Meta:
        unique_together = ["listing", "date"]
