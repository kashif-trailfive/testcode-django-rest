from django.db import models
from rest_framework.exceptions import APIException


class Listing(models.Model):
    HOTEL = "hotel"
    APARTMENT = "apartment"
    LISTING_TYPE_CHOICES = (
        ("hotel", "Hotel"),
        ("apartment", "Apartment"),
    )

    listing_type = models.CharField(
        max_length=16, choices=LISTING_TYPE_CHOICES, default=APARTMENT
    )
    title = models.CharField(
        max_length=255,
    )
    country = models.CharField(
        max_length=255,
    )
    city = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.title


class HotelRoomType(models.Model):
    hotel = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="hotel_room_types",
    )
    title = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f"{self.hotel} - {self.title}"


class HotelRoom(models.Model):
    hotel_room_type = models.ForeignKey(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="hotel_rooms",
    )
    room_number = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.room_number


class BookingInfo(models.Model):
    listing = models.OneToOneField(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="booking_info",
    )
    hotel_room_type = models.OneToOneField(
        HotelRoomType,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="booking_info",
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        if self.listing:
            obj = self.listing
        else:
            obj = self.hotel_room_type

        return f"{obj} {self.price}"

    def get_listing_type(self):
        if self.listing:
            return self.listing.listing_type
        else:
            return self.hotel_room_type.hotel.listing_type

    def get_listing_title(self):
        if self.listing:
            return self.listing.title
        else:
            return self.hotel_room_type.hotel.title

    def get_listing_country(self):
        if self.listing:
            return self.listing.country
        else:
            return self.hotel_room_type.hotel.country

    def get_listing_city(self):
        if self.listing:
            return self.listing.city
        else:
            return self.hotel_room_type.hotel.city


class Reservation(models.Model):
    booking_info = models.ForeignKey(BookingInfo, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"from {self.check_in} to {self.check_out}"

    def save(self, *args, **kwargs):
        """
        on save validate start date and end date
        """
        if self.check_in and self.check_out:
            if self.check_in >= self.check_out:
                raise APIException("Check-in date must be before check-out date")
        super(Reservation, self).save(*args, **kwargs)
