from django.urls import path
from .views import ReservationsReportView

app_name = "listing"

urlpatterns = [
    path("listing/reservations-report/", ReservationsReportView.as_view(), name="reservations_report"),
]
