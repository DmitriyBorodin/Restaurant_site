from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DeleteView, ListView, DetailView
from urllib3 import request

from booking.forms import ReservationForm
from booking.models import Reservation


class IndexView(TemplateView):
    template_name = "booking/main.html"


class AboutView(TemplateView):
    template_name = "booking/about_us.html"


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('booking:index_page')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Сохраняем форму
        response = super().form_valid(form)

        # Добавляем сообщение об успешной брони
        messages.success(self.request, 'Столик забронирован! Уже ждём вас :)')

        # Возвращаем стандартное поведение
        return response

class ReservationListView(ListView):
    model = Reservation


class ReservationDetailView(DetailView):
    model = Reservation


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    success_url = '/users/profile/'


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy("users:profile")
    login_url = '/users/login/'
    context_object_name = 'reservation'
