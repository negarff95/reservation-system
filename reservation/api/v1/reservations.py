import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from core.http import JsonResponse
from listing.models import Listing
from reservation.models import Reservation
from reservation.serializers.v1 import ReservationSerializer, ReservationInput


logger = logging.getLogger("reservation")
User = get_user_model()


class Reservations(APIView):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(request_body=ReservationInput)
    def post(self, request):
        self.exception_data = {"status": 400, "message": "missing required entries."}
        data = {}
        serializer = ReservationInput(data=request.data)
        if serializer.is_valid():
            data = serializer.data

        num_rooms = data["num_rooms"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        listing_id = data["listing_id"]
        username = data["name"]
        special_requests = (
            data["special_requests"] if "special_requests" in data else None
        )

        self.exception_data = {"status": 404, "message": "listing not found."}
        listing = Listing.objects.get(id=listing_id)
        user = User.objects.get_or_create(username=username)[0]

        is_available, exception = listing.is_available(num_rooms, start_date, end_date)

        if is_available:
            self.exception_data = {}
            reservation = Reservation.objects.create(
                num_rooms=num_rooms,
                listing=listing,
                customer=user,
                start_date=start_date,
                end_date=end_date,
                special_requests=special_requests,
            )
            return JsonResponse(
                status=201,
                data=ReservationSerializer(reservation).data,
                message="Your reservation has been successfully completed.",
            )
        return JsonResponse(status=409, message=exception)
