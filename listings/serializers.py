from rest_framework import serializers

from listings.models import BookingInfo, Reservation


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
        fields = "__all__"
