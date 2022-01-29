from rest_framework import serializers

from rest_framework.exceptions import APIException

from listings.models import BookingInfo, Reservation, HotelRoom

from django.db.models import Q

from datetime import datetime

class BookingInfoSerializer(serializers.ModelSerializer):
    """
    BookingInfoSerializer
    """

    listing_type = serializers.CharField(read_only=True, source="get_listing_type")
    title = serializers.CharField(read_only=True, source="get_listing_title")
    country = serializers.CharField(read_only=True, source="get_listing_country")
    city = serializers.CharField(read_only=True, source="get_listing_city")

    class Meta:

        model = BookingInfo
        fields = ["listing_type", "title", "country", "city", "price"]


class ReservationSerializer(serializers.ModelSerializer):
    """
    ReservationSerializer
    """

    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):

        """
        Check that check_in is before check_out or less than today.
        """
        present = datetime.now()
        if data['check_in'] < present.date():
            raise serializers.ValidationError("Date must be greater or equal than today")

        if data['check_in'] > data['check_out']:
            raise serializers.ValidationError("check_out must occur after check_in")
        
        """
        Check that room to book belong to a selected hotel.
        """
        try:
            data_booking = BookingInfo.objects.get(id=data['booking_info'].id)
            listing_type = data_booking.get_listing_type()
            if(listing_type == "hotel"):
                data_room = HotelRoom.objects.get(id=data['hotel_room'].id)
                if(data_room.hotel_room_type.hotel != data_booking.hotel_room_type.hotel):
                    raise serializers.ValidationError("Invalid Room Number")
        except Exception as e:
            raise APIException('Provide booking info- Hotel or Apartment')


        """
        Check that room already booked.
        """
        data_booking = BookingInfo.objects.get(id=data['booking_info'].id)
        listing_type = data_booking.get_listing_type()
        
        if(listing_type == "apartment"):

            reservations = Reservation.objects.filter( Q(booking_info=data['booking_info'].id)
                                                      & Q(check_in__gte=data['check_in'], check_in__lte=data['check_out'])
                                                      & Q(check_out__gte=data['check_in'], check_out__lte=data['check_out'])
                                                     )

            if reservations.count() > 0 :
                raise serializers.ValidationError("Apartment Already Booked")


        """
        Check that hotel or hotel room already booked.
        """
        if(listing_type == "hotel"):

            reservations = Reservation.objects.filter( Q(booking_info=data['booking_info'].id)
                                                      & Q(check_in__gte=data['check_in'], check_in__lte=data['check_out'])
                                                      & Q(check_out__gte=data['check_in'], check_out__lte=data['check_out'])
                                                      & Q(hotel_room = data['hotel_room'])
                                                     )

            if reservations.count() > 0 :
                raise serializers.ValidationError("Hotel Already Booked")

        '''Price Calculator'''
        try:
            delta = data['check_out'] - data['check_in']
            data['total_price'] = data_booking.price * delta.days
        except Exception as e:
            raise APIException(e)

        return data