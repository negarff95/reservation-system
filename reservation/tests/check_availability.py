from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from listing.models import Listing
from django.contrib.auth import get_user_model

User = get_user_model()


class CheckAvailabilityAPITestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create(username="user_test")
        self.listing = Listing.objects.create(
            name="Test Listing",
            owner=self.owner,
            address="123 Main St",
            total_rooms=5,
            price_per_room=100.0,
            description="A great place to stay",
            amenities="Wi-Fi, TV, AC",
        )

        self.url = reverse("reservation:v1:check_availability")

        self.valid_data = {
            "num_rooms": 2,
            "listing_id": self.listing.id,
            "start_date": "2023-10-15",
            "end_date": "2023-10-18",
        }

    def test_check_availability_api(self):
        client = APIClient()

        response = client.get(self.url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_check_availability_api_invalid_data(self):
        client = APIClient()

        invalid_data = {
            "num_rooms": 2,
            "start_date": "2023-10-15",
        }

        response = client.get(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_availability_api_listing_not_found(self):
        client = APIClient()

        invalid_data = {
            "num_rooms": 2,
            "listing_id": 999,
            "start_date": "2023-10-15",
            "end_date": "2023-10-18",
        }

        response = client.get(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

