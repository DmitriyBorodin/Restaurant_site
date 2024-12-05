from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from booking.models import Reservation
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, Feedback


class ProfileTemplateView(TemplateView):
    """View для страницы профиля пользователя"""
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        # Получаем текущего пользователя
        context = super().get_context_data(**kwargs)

        # Запрашиваем все резервации для текущего пользователя
        reservations = Reservation.objects.filter(owner=self.request.user)

        # Добавляем queryset в контекст, чтобы можно было итерировать по нему в шаблоне
        context['reservations'] = reservations
        return context


class UserRegisterView(CreateView):
    """View для создания пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        # Сначала сохраняем пользователя
        response = super().form_valid(form)

        # Проверяем наличие параметра `next` в запросе
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)  # Перенаправляем на `next`, если он указан

        # Если параметра `next` нет, используем стандартный `success_url`
        return response


class ProfileView(UpdateView):
    """View для обновления информации пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class FeedbackCreateView(CreateView):
    """View для создания обратной связи"""
    model = Feedback
    fields = ['name', 'phone', 'message']
    success_url = reverse_lazy('booking:index_page')
