import datetime
from django.test import TestCase

from listings.models import Listing, HotelRoomType, HotelRoom, BookingInfo, Reservation

# testing the Reservation model
class ReservationTestCase(TestCase):
    def setUp(self):
        self.listing = Listing.objects.create(
            title="Test Listing",
            country="Test Country",
            city="Test City",
            listing_type="hotel",
        )
        self.hotel_room_type = HotelRoomType.objects.create(
            hotel=self.listing,
            title="Test Hotel Room Type",
        )
        self.hotel_room = HotelRoom.objects.create(
            hotel_room_type=self.hotel_room_type,
            room_number="1",
        )
        self.booking_info = BookingInfo.objects.create(
            listing=self.listing,
            hotel_room_type=self.hotel_room_type,
            price=100,
        )

    def test_post(self):
        self.assertEqual(Reservation.objects.count(), 0)
        Reservation.objects.create(
            check_in="2022-01-25",
            check_out="2022-01-28",
            booking_info=self.booking_info,
        )
        self.assertEqual(
            Reservation.objects.count(), 1, msg="Reservation was not created"
        )
        self.assertEqual(
            Reservation.objects.first().check_in,
            datetime.date(2022, 1, 25),
            msg="Check in date is not correct",
        )
        self.assertEqual(
            Reservation.objects.first().check_out,
            datetime.date(2022, 1, 28),
            msg="Check out date is not correct",
        )
        self.assertEqual(
            Reservation.objects.first().booking_info,
            self.booking_info,
            msg="Booking info is not correct",
        )
