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

    reserved_table = models.ForeignKey(Table, on_delete=models.SET_NULL, related_name='reservations', **NULLABLE)
    reservation_date = models.DateField(verbose_name='Забронированная дата')
    reservation_start = models.TimeField(verbose_name='Забронированное время')
    guests_amount = models.PositiveIntegerField(default=1, verbose_name='Количество гостей')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")
    reservation_number = models.CharField(max_length=6, null=True, blank=True, unique=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Владелец брони", **NULLABLE)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self):
        if not self.reservation_number:
            self.reservation_number = self.id_generator()
            while Reservation.objects.filter(urlhash=self.reservation_number).exists():
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
