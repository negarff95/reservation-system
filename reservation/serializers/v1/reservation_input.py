from rest_framework import serializers


class ReservationInput(serializers.Serializer):
    num_rooms = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    listing_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    special_requests = serializers.CharField(required=False)


class CheckAvailabilityInput(serializers.Serializer):
    num_rooms = serializers.IntegerField(required=True)
    listing_id = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)