from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DeleteView, ListView, DetailView

from booking.forms import ReservationForm
from booking.models import Reservation


class IndexView(TemplateView):
    template_name = "booking/main.html"


class AboutView(TemplateView):
    template_name = "booking/about_us.html"


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('booking:index_page')

class ReservationListView(ListView):
    model = Reservation


class ReservationDetailView(DetailView):
    model = Reservation


class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm


class ReservationDeleteView(DeleteView):
    model = Reservation
    success_url = reverse_lazy("booking:reservation_list")
