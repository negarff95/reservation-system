from django.test import TestCase
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from listing.models import Listing
from reservation.models import ReservedDate


User = get_user_model()


class ListingModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owneruser", password="ownerpassword")
        self.customer = User.objects.create_user(username="customeruser", password="customerpassword")
        self.listing = Listing.objects.create(
            owner=self.owner,
            name="Test Listing",
            address="123 Main St",
            total_rooms=5,
            price_per_room=100.0,
        )

    def create_reserved_date(self, date, num_rooms_reserved):
        return ReservedDate.objects.create(
            listing=self.listing,
            date=date,
            num_rooms_reserved=num_rooms_reserved,
        )

    def test_is_available_with_one_day_fully_booked(self):
        start_date = date(2023, 10, 15)
        end_date = date(2023, 10, 18)

        # Create a reserved date that fully books the rooms for one day
        self.create_reserved_date(start_date, 5)

        num_rooms_required = 2
        is_available, message = self.listing.is_available(num_rooms_required, start_date, end_date)

        self.assertFalse(is_available)
        expected_message = f"Rooms are fully booked from date {start_date} to date {end_date}"
        self.assertEqual(message, expected_message)

    def test_is_available_with_one_day_partially_booked(self):
        start_date = date(2023, 10, 15)
        end_date = date(2023, 10, 18)

        # Create a reserved date that partially books the rooms for one day
        self.create_reserved_date(start_date, 3)

        num_rooms_required = 2
        is_available, message = self.listing.is_available(num_rooms_required, start_date, end_date)

        self.assertTrue(is_available)
        self.assertEqual(message, "")

    def test_is_available_with_multiple_days_fully_booked(self):
        start_date = date(2023, 10, 15)
        end_date = date(2023, 10, 18)

        # Create reserved dates that fully book the rooms for multiple days
        self.create_reserved_date(start_date, 5)
        self.create_reserved_date(start_date + timedelta(days=2), 5)

        num_rooms_required = 2
        is_available, message = self.listing.is_available(num_rooms_required, start_date, end_date)

        self.assertFalse(is_available)
        expected_message = f"Rooms are fully booked from date {start_date} to date {end_date}"
        self.assertEqual(message, expected_message)

    def test_is_available_with_multiple_days_partially_booked(self):
        start_date = date(2023, 10, 15)
        end_date = date(2023, 10, 18)

        # Create reserved dates that partially book the rooms for multiple days
        self.create_reserved_date(start_date, 3)
        self.create_reserved_date(start_date + timedelta(days=2), 2)

        num_rooms_required = 2
        is_available, message = self.listing.is_available(num_rooms_required, start_date, end_date)

        self.assertTrue(is_available)
        self.assertEqual(message, "")
