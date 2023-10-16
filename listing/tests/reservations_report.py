from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from listing.models import Listing
from reservation.models import Reservation

User = get_user_model()


class ReservationsReportViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.listing = Listing.objects.create(
            owner=self.user,
            name="Test Listing",
            address="123 Main St",
            total_rooms=5,
            price_per_room=100.0,
        )

    def test_reservations_report_with_listing_id(self):
        Reservation.objects.create(
            num_rooms=2,
            listing=self.listing,
            customer=self.user,
            start_date="2023-10-15",
            end_date="2023-10-18",
        )

        # Get the URL for the ReservationsReportView with the listing ID
        url = reverse("listing:reservations_report") + f"?listing={self.listing.id}"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check if the listing and reservation are in the response context
        self.assertEqual(response.context["listing"], self.listing)
        self.assertEqual(list(response.context["reservations"]), [self.listing.reservations.first()])

    def test_reservations_report_with_listing_name(self):
        Reservation.objects.create(
            num_rooms=2,
            listing=self.listing,
            customer=self.user,
            start_date="2023-10-15",
            end_date="2023-10-18",
        )

        url = reverse("listing:reservations_report") + f"?listing={self.listing.name}"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check if the listing and reservation are in the response context
        self.assertEqual(response.context["listing"], self.listing)
        self.assertEqual(list(response.context["reservations"]), [self.listing.reservations.first()])

    def test_reservations_report_listing_not_found(self):
        url = reverse("listing:reservations_report") + "?listing=999"

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Check that no listing or reservations are in the response context
        self.assertIsNone(response.context.get("listing"))
        self.assertIsNone(response.context.get("reservations"))
