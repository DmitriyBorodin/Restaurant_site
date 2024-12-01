from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = PhoneNumberField(unique=True, verbose_name="Телефон")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя отправителя')
    phone = models.CharField(max_length=20, verbose_name='Телефон отправителя')
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"

    def __str__(self):
        return f'Обратная связь от {self.name} ({self.phone}):\n{self.message}'