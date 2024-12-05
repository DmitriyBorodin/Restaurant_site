import string
import random

from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}

class Table(models.Model):

    TABLE_SIZE_CHOICES = (
        ('Small', 'На 1-2 персон'),
        ('Big', 'На 3+ персон'),
    )

    RESERVATION_STATUS_CHOICES = (
        ('Available', 'Доступен'),
        ('Reserved', 'Забронирован'),
    )

    table_status = models.CharField(max_length=255,
                                          choices=RESERVATION_STATUS_CHOICES,
                                          verbose_name='Статус бронирования стола', default='Available')
    table_number = models.PositiveIntegerField(unique=True, verbose_name='Номер стола')
    table_size = models.CharField(max_length=255, choices=TABLE_SIZE_CHOICES, verbose_name='Размер стола')

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return (f'Номер стола - {self.table_number}, '
                f'размер стола - {self.table_size}')


class Reservation(models.Model):

    GUEST_AMOUNT_CHOICES = (
        ('1-2', '1-2'),
        ('3-4', '3-4'),
        ('4+', '4+'),
    )

    RESERVATION_STATUS_CHOICES = (
        ('Активна', 'Активна'),
        ('Истекла', 'Истекла'),
        ('Отменена', 'Отменена'),
    )

    reservation_date = models.DateField(verbose_name='Дата')
    reservation_start = models.TimeField(verbose_name='Время')
    guests_amount = models.CharField(default='1-2', choices=GUEST_AMOUNT_CHOICES, verbose_name='Количество гостей')
    reservation_commentary = models.CharField(max_length=255, verbose_name='Пожелания к брони', **NULLABLE)

    reservation_status = models.CharField(default='Активна', choices=RESERVATION_STATUS_CHOICES, verbose_name='Статус брони')
    reserved_table = models.ForeignKey(Table, on_delete=models.SET_NULL, related_name='reserved_table', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")
    reservation_number = models.CharField(max_length=6, null=True, blank=True, unique=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="reservation_owner", **NULLABLE)

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            self.reservation_number = self.id_generator()
            while Reservation.objects.filter(reservation_number=self.reservation_number).exists():
                self.reservation_number = self.id_generator()
        super(Reservation, self).save()

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"

    def __str__(self):
        return (f'Дата брони - {self.reservation_date}, '
                f'время брони - {self.reservation_start}, '
                f'владелец брони - {self.owner},'
                f'номер брони - {self.reservation_number}')
