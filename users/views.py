from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, Feedback


class ProfileTemplateView(TemplateView):
    template_name = "users/profile.html"


class UserRegisterView(CreateView):
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
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class FeedbackCreateView(CreateView):
    model = Feedback
    fields = ['name', 'phone', 'message']
    success_url = reverse_lazy('booking:index_page')