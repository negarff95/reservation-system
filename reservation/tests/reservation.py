from django.test import TestCase
from datetime import date, timedelta
from django.contrib.auth import get_user_model

from constants import ReservationStatus
from listing.models import Listing
from reservation.models import Reservation, ReservedDate

User = get_user_model()


class ReservationModelTest(TestCase):
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

    def create_reserved_date(self, _date, num_rooms_reserved):
        return ReservedDate.objects.create(
            listing=self.listing,
            date=_date,
            num_rooms_reserved=num_rooms_reserved,
        )

    def test_str_method(self):
        reservation = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=2,
        )

        expected_str = f"{reservation.listing.name}/{reservation.customer.username}"
        self.assertEqual(str(reservation), expected_str)

    def test_total_price_calculation(self):
        reservation = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=3,
        )

        # Check if the total_price is calculated correctly
        expected_total_price = 3 * self.listing.price_per_room
        self.assertEqual(reservation.total_price, expected_total_price)

    def test_change_reserved_rooms_number_create(self):
        reservation = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=2,
        )

        # Check if the ReservedDate instances have the correct num_rooms_reserved
        reserved_dates = ReservedDate.objects.filter(
            listing=self.listing,
        )
        self.assertEqual(reserved_dates.count(), 3)  # Three days in the date range
        for reserved_date in reserved_dates:
            self.assertEqual(reserved_date.num_rooms_reserved, 2)

    def test_change_reserved_rooms_number_update(self):
        reservation_1 = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=2,
        )

        # Check if the ReservedDate instances have the correct num_rooms_reserved
        reserved_dates = ReservedDate.objects.filter(listing=self.listing)

        self.assertEqual(reserved_dates.count(), 3)  # Three days in the date range
        for reserved_date in reserved_dates:
            self.assertEqual(reserved_date.num_rooms_reserved, 2) #

        # Create reservation_2 in same date with reservation_1
        reservation_2 = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=3,
        )

        total_reserved_rooms = reservation_1.num_rooms + reservation_2.num_rooms
        reserved_dates = ReservedDate.objects.filter(listing=self.listing)

        # Check if the ReservedDate instances have the correct num_rooms_reserved after update
        self.assertEqual(reserved_dates.count(), 3)  # Three days in the date range
        for reserved_date in reserved_dates:
            self.assertEqual(reserved_date.num_rooms_reserved, total_reserved_rooms)

    def test_change_reservation_status(self):
        reservation = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=2,
        )

        reserved_dates = ReservedDate.objects.filter(listing=self.listing)
        for reserved_date in reserved_dates:
            self.assertEqual(reserved_date.num_rooms_reserved, 2)

        # Try to update the reserved rooms number by changing status to canceled
        reservation.status = ReservationStatus.Canceled
        reservation.save()

        reserved_dates = ReservedDate.objects.filter(listing=self.listing)

        for reserved_date in reserved_dates:
            self.assertEqual(reserved_date.num_rooms_reserved, 0)

        # Try to change the status to something other than Canceled
        reservation.status = ReservationStatus.Pending

        with self.assertRaises(Exception):
            reservation.save()

    def test_delete_reservation_not_allowed(self):
        reservation = Reservation.objects.create(
            listing=self.listing,
            customer=self.customer,
            start_date=date(2023, 10, 15),
            end_date=date(2023, 10, 18),
            num_rooms=2,
        )

        with self.assertRaises(Exception):
            reservation.delete()
