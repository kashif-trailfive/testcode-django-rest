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

            if max_price:
                queryset = BookingInfo.objects.filter(price__lte=max_price)
            else:
                queryset = BookingInfo.objects.all()
            queryset = queryset.select_related("listing", "hotel_room_type")
            if check_in and check_out:
                reserved_listing = Reservation.objects.filter(
                    Q(check_in__gte=check_in, check_in__lte=check_out)
                    | Q(check_out__gte=check_in, check_out__lte=check_out)
                )
                for item in reserved_listing:
                    if item.hotel_room:
                        hotel_rooms = HotelRoom.objects.filter(
                            hotel_room_type=item.hotel_room.hotel_room_type
                        )
                        reserved_rooms = reserved_listing.filter(
                            booking_info__hotel_room_type=item.hotel_room.hotel_room_type
                        )
                        if len(hotel_rooms) > len(reserved_rooms):
                            pass
                        else:
                            queryset = queryset.exclude(
                                hotel_room_type=item.booking_info.hotel_room_type
                            )

                queryset = queryset.order_by("-price")

            hotels_list = queryset.filter(
                hotel_room_type__hotel__listing_type="hotel"
            ).values_list("id", flat=True)
            if hotels_list:
                for id in hotels_list:
                    hotel_id = queryset.filter(id=id).values_list(
                        "hotel_room_type__hotel__id", flat=True
                    )
                    hotel_List = queryset.filter(hotel_room_type__hotel__id=hotel_id[0])
                    if len(hotel_List) > 1:
                        queryset = queryset.exclude(id=id)

            return queryset.order_by("price")

        except Exception as e:
            raise APIException(e)

# Run URL below
# http://localhost:8000/api/v1/makereservation/
class ReservationInfoViewSet(generics.ListCreateAPIView):
    """
    ReservationInfoViewSet
    """

    try:
        serializer_class = ReservationSerializer
        queryset = Reservation.objects.all()
    except Exception as e:
        raise APIException(e)
