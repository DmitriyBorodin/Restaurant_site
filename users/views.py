from django.shortcuts import render
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