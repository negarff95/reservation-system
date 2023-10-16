from django.urls import include, path

app_name = "reservation"

urlpatterns = [
    path("api/v1/reservation/", include("reservation.api.v1.urls", namespace="v1")),
]
