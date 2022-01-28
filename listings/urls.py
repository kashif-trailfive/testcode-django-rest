"""
RestInterface/urls.py
"""
from django.urls import path

from listings.views import BookingInfoViewSet, ReservationInfoViewSet

urlpatterns = [
    path("units/", BookingInfoViewSet.as_view(), name="units"),
    path("makereservation/", ReservationInfoViewSet.as_view()),
]
