from curses.ascii import NUL
from django.db.models import Q
from rest_framework import generics
from listings.models import BookingInfo, Reservation, HotelRoom
from listings.serializers import BookingInfoSerializer, ReservationSerializer

from rest_framework.exceptions import APIException


# Run URL below
# http://localhost:8000/api/v1/units/?max_price=100&check_in=2022-01-25&check_out=2022-01-28
class BookingInfoViewSet(generics.ListAPIView):
    """
    BookingInfoViewSet
    """

    serializer_class = BookingInfoSerializer

    def get_queryset(self):
        """
        First filter over max price then filter over check in and check out
        """

        try:

            max_price = self.request.query_params.get("max_price")
            check_in = self.request.query_params.get("check_in")
            check_out = self.request.query_params.get("check_out")

            queryset = BookingInfo.objects.all()

            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if check_in and check_out:
                reserved_listing = Reservation.objects.filter(
                    Q(check_in__gte=check_in, check_in__lte=check_out)
                    | Q(check_out__gte=check_in, check_out__lte=check_out)
                )
                
                
                '''Filer Booking on basis of hotel room and apartment'''
                hotel_rooms = HotelRoom.objects.all()

                for item in reserved_listing:
                    if(item.hotel_room):
                        for room in hotel_rooms:
                            if(room.id == item.hotel_room):
                                queryset = queryset.exclude(hotel_room_type=room.hotel_room_type)
           
                    else:
                        queryset = queryset.exclude(id__in=[item.booking_info.id for item in reserved_listing])
          

            queryset = queryset.select_related("listing", "hotel_room_type")
            return queryset.order_by("price")

        except Exception as e:
            raise APIException(e)


class ReservationInfoViewSet(generics.ListCreateAPIView):
    """
    ReservationInfoViewSet
    """

    try:
        serializer_class = ReservationSerializer
        queryset = Reservation.objects.all()
    except Exception as e:
        raise APIException(e)
