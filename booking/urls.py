from django.urls import path
from booking.apps import BookingConfig
from booking.views import IndexView, AboutView
from django.conf.urls.static import static
from config import settings

app_name = BookingConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index_page"),
    path("about/", AboutView.as_view(), name="about_page"),
]
