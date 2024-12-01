import string
import random

from django.db import models

NULLABLE = {"blank": True, "null": True}

class Reservation(models.Model):

    RESERVATION_STATUS_CHOICES = (
        ('Free', 'Свободен'),
        ('Reserved', 'Забронирован'),
    )

    reservation_status = models.CharField(max_length=255, choices=RESERVATION_STATUS_CHOICES, verbose_name='Статус бронирования стола')
    reservation_date = models.DateField(verbose_name='Забронированная дата')
    reservation_start = models.TimeField(verbose_name='Забронированное время')
    reservation_duration = models.TimeField(verbose_name='Продолжительность бронирования')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания бронирования")
    reservation_number = models.CharField(max_length=6, null=True, blank=True, unique=True)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self):
        if not self.reservation_number:
            # Generate ID once, then check the db. If exists, keep trying.
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
                f'статус бронирования стола - {self.reservation_status},'
                f'номер брони - {self.reservation_number}')


class Table(models.Model):

    TABLE_SIZE_CHOICES = (
        ('Small', 'На 1-2 персон'),
        ('Big', 'На 3+ персон'),
    )

    table_number = models.PositiveIntegerField(unique=True, verbose_name='Номер стола')
    table_size = models.CharField(max_length=255, choices=TABLE_SIZE_CHOICES, verbose_name='Размер стола')
    table_status = models.ForeignKey(Reservation, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

    def __str__(self):
        return (f'Номер стола - {self.table_number}, '
                f'размер стола - {self.table_size}, '
                f'статус бронирования стола - {self.table_status}')
