from django.contrib import admin
from reservation.models import Reservation, ReservedDate

admin.site.register(Reservation)
admin.site.register(ReservedDate)
