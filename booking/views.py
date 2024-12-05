from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DeleteView, ListView, DetailView
from urllib3 import request

from booking.forms import ReservationForm
from booking.models import Reservation, Table
from booking.permissions import IsOwner


class IndexView(TemplateView):
    template_name = "booking/main.html"


class AboutView(TemplateView):
    template_name = "booking/about_us.html"


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('booking:index_page')
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        # Получаем текущего пользователя
        context = super().get_context_data(**kwargs)
        # Запрашиваем все резервации для текущего пользователя
        reservations = Table.objects.all()
        # Добавляем queryset в контекст, чтобы можно было итерировать по нему в шаблоне
        context['tables'] = reservations
        return context

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
    permission_classes = [IsOwner]


class ReservationDetailView(DetailView):
    model = Reservation
    permission_classes = [IsOwner]


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    success_url = '/users/profile/'
    permission_classes = [IsOwner]


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy("users:profile")
    login_url = '/users/login/'
    context_object_name = 'reservation'
    permission_classes = [IsOwner]
