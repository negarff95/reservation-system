from rest_framework.serializers import ModelSerializer
from reservation.models import Reservation


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "listing",
            "customer",
            "start_date",
            "end_date",
            "total_price",
            "num_rooms",
            "special_requests",
            "status"
        )
