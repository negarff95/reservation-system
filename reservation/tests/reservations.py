from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from listing.models import Listing
from reservation.models import Reservation


User = get_user_model()


class ReservationsAPITestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owneruser", password="ownerpassword")
        self.listing = Listing.objects.create(
            owner=self.owner,
            name="Test Listing",
            address="123 Main St",
            total_rooms=5,
            price_per_room=100.0,
        )
        self.valid_data = {
            "num_rooms": 2,
            "listing_id": self.listing.id,
            "start_date": "2023-10-15",
            "end_date": "2023-10-18",
            "name": "John Doe",
        }
        self.invalid_data = {}  # Invalid data for testing missing required fields

    def test_create_reservation_valid(self):
        url = reverse("reservation:v1:reservations")
        self.client.login(username="customeruser", password="customerpassword")

        response = self.client.post(url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reservation = Reservation.objects.get()
        self.assertEqual(reservation.num_rooms, self.valid_data["num_rooms"])
        self.assertEqual(reservation.listing, self.listing)
        self.assertEqual(reservation.customer.username, self.valid_data['name'])
        self.assertEqual(reservation.start_date, date.fromisoformat(self.valid_data["start_date"]))
        self.assertEqual(reservation.end_date, date.fromisoformat(self.valid_data["end_date"]))
        self.assertEqual(reservation.special_requests, self.valid_data.get("special_requests"))

    def test_create_reservation_invalid(self):
        url = reverse("reservation:v1:reservations")
        self.client.login(username="customeruser", password="customerpassword")

        response = self.client.post(url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_listing_not_found(self):
        url = reverse("reservation:v1:reservations")
        self.client.login(username="customeruser", password="customerpassword")

        invalid_data = self.valid_data.copy()
        invalid_data["listing_id"] = 999  # An invalid listing ID

        response = self.client.post(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
