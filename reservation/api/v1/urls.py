from django.urls import path
from reservation.api.v1 import Reservations, CheckAvailability

app_name = "reservation"

urlpatterns = [
    path("reservations/", Reservations.as_view(), name="reservations"),
    path("check-availability/", CheckAvailability.as_view(), name="check_availability")
]
