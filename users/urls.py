from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegisterView, ProfileView, FeedbackCreateView, \
    ProfileTemplateView

app_name = UsersConfig.name

urlpatterns = [
    path("profile/", ProfileTemplateView.as_view(), name="profile"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('me/', ProfileView.as_view(), name='me'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
]
