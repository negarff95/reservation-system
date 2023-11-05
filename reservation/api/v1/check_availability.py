import logging
from drf_yasg.utils import swagger_auto_schema
from datetime import date


from rest_framework.views import APIView

from core.http import JsonResponse
from listing.models import Listing
from reservation.serializers.v1 import CheckAvailabilityInput


logger = logging.getLogger("reservation")


class CheckAvailability(APIView):
    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(query_serializer=CheckAvailabilityInput)
    def get(self, request):
        self.exception_data = {"status": 400, "message": "missing required entries."}
        serializer = CheckAvailabilityInput(data=request.query_params)
        query_params = {}

        if serializer.is_valid():
            query_params = serializer.data

        num_rooms = query_params["num_rooms"]
        listing_id = query_params["listing_id"]
        start_date = query_params["start_date"]
        end_date = query_params["end_date"]

        self.exception_data = {"status": 404, "message": "listing not found."}
        listing = Listing.objects.get(id=listing_id)

        if type(start_date) == str:
            start_date = date.fromisoformat(start_date)
        if type(end_date) == str:
            end_date = date.fromisoformat(end_date)

        if start_date > end_date or start_date < date.today():
            status = 409
            message = "invalid start date and end date"
            return JsonResponse(status=status, message=message)

        is_available, exception = listing.is_available(num_rooms, start_date, end_date)

        if is_available:
            status = 200
            message = "Rooms are available from date {} to {}".format(
                start_date, end_date
            )
        else:
            status = 409
            message = exception

        return JsonResponse(status=status, message=message)
