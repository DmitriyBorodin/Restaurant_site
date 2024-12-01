from django.urls import path
from booking.apps import BookingConfig
from booking.views import IndexView

app_name = BookingConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index_page"),
]
