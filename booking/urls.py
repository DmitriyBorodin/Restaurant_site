from django.urls import path
from booking.apps import BookingConfig
from booking.views import IndexView, AboutView, ReservationCreateView, \
    ReservationListView, ReservationDetailView, ReservationUpdateView, \
    ReservationDeleteView

app_name = BookingConfig.name

urlpatterns = [
    path("", IndexView.as_view(), name="index_page"),
    path("about/", AboutView.as_view(), name="about_page"),
    path("reservation/create/", ReservationCreateView.as_view(), name="reservation_create"),
    path("reservation/", ReservationListView.as_view(), name="reservation_list"),
    path("reservation/<int:pk>/", ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservation/update/<int:pk>/", ReservationUpdateView.as_view(), name="reservation_update"),
    path("reservation/delete/<int:pk>/", ReservationDeleteView.as_view(), name="reservation_delete"),
]
