import json

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.http import JsonResponse

from listings.models import BookingInfo, Reservation, Listing, HotelRoomType, HotelRoom

# test the endpoint
class TestBookingInfoViewSetTest(APITestCase):
    """
    BookingInfoViewSetTest
    """

    def setUp(self):
        self.listing = Listing.objects.create(
            title="Test Listing",
            country="Test Country",
            city="Test City",
            listing_type="hotel",
        )
        self.hotel_room_type_one = HotelRoomType.objects.create(
            hotel=self.listing,
            title="Test Hotel Room Type 1",
        )
        self.hotel_room_type_two = HotelRoomType.objects.create(
            hotel=self.listing,
            title="Test Hotel Room Type 2",
        )
        self.hotel_room_type_three = HotelRoomType.objects.create(
            hotel=self.listing,
            title="Test Hotel Room Type 3",
        )
        HotelRoom.objects.create(
            hotel_room_type=self.hotel_room_type_one,
            room_number="1",
        )
        HotelRoom.objects.create(
            hotel_room_type=self.hotel_room_type_two,
            room_number="2",
        )
        HotelRoom.objects.create(
            hotel_room_type=self.hotel_room_type_three, room_number="3"
        )

        self.booking_info_one = BookingInfo.objects.create(
            hotel_room_type=self.hotel_room_type_one,
            price=50,
        )
        self.booking_info_two = BookingInfo.objects.create(
            hotel_room_type=self.hotel_room_type_two,
            price=60,
        )
        self.booking_info_three = BookingInfo.objects.create(
            hotel_room_type=self.hotel_room_type_three,
            price=200,
        )

    url = reverse("listings:units")

    def verify_response(
        self, response, ex_status=200, ex_type=JsonResponse, ex_json_data=None
    ):
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, ex_status)
        self.assertTrue(isinstance(response, ex_type))
        if ex_json_data is not None:
            data = json.loads(response.content)
            self.assertDictEqual(ex_json_data, data)

    def test_list_booking_below_max_price(self):
        """
        test checking below Max price 100
        """
        client = APIClient()
        response = client.get(
            self.url,
            {"max_price": "100", "check_in": "2022-01-22", "check_out": "2022-01-25"},
        )
        self.verify_response(
            response=response,
            ex_type=Response,
            ex_json_data={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "50.00",
                        "title": "Test Listing",
                    },
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "60.00",
                        "title": "Test Listing",
                    },
                ],
            },
        )

    def test_list_booking_above_max_price(self):
        """
        test create booking info with Max price 200
        """
        client = APIClient()
        response = client.get(
            self.url,
            {"max_price": "200", "check_in": "2022-01-22", "check_out": "2022-01-25"},
        )
        self.verify_response(
            response=response,
            ex_type=Response,
            ex_json_data={
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "50.00",
                        "title": "Test Listing",
                    },
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "60.00",
                        "title": "Test Listing",
                    },
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "200.00",
                        "title": "Test Listing",
                    },
                ],
            },
        )

    def test_list_booking_with_blocked_day(self):
        """
        test create booking info with Max price 200
        """
        Reservation.objects.create(
            booking_info=self.booking_info_one,
            check_in="2022-01-23",
            check_out="2022-01-24",
        )
        client = APIClient()
        response = client.get(
            self.url,
            {"max_price": "200", "check_in": "2022-01-22", "check_out": "2022-01-26"},
        )
        self.verify_response(
            response=response,
            ex_type=Response,
            ex_json_data={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "60.00",
                        "title": "Test Listing",
                    },
                    {
                        "city": "Test City",
                        "country": "Test Country",
                        "listing_type": "hotel",
                        "price": "200.00",
                        "title": "Test Listing",
                    },
                ],
            },
        )
