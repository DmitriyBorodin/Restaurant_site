from datetime import date, time, timedelta

from django.test import TestCase
from django.utils import timezone

from booking.forms import ReservationForm
from booking.models import Table, Reservation
from users.models import User


class TableModelTest(TestCase):
    def setUp(self):
        """Создаём тестовый объект модели Table."""
        self.table = Table.objects.create(
            table_status='Available',
            table_number=1,
            table_size='Small'
        )

    def test_table_creation(self):
        """Тест: объект модели создаётся корректно."""
        self.assertEqual(self.table.table_status, 'Available')
        self.assertEqual(self.table.table_number, 1)
        self.assertEqual(self.table.table_size, 'Small')

    def test_str_method(self):
        """Тест: метод __str__ возвращает ожидаемую строку."""
        self.assertEqual(
            str(self.table),
            'Номер стола - 1, размер стола - Small'
        )

    def test_table_status_choices(self):
        """Тест: поле table_status имеет валидные значения выбора."""
        choices = dict(Table.RESERVATION_STATUS_CHOICES)
        self.assertIn(self.table.table_status, choices.keys())

    def test_table_size_choices(self):
        """Тест: поле table_size имеет валидные значения выбора."""
        choices = dict(Table.TABLE_SIZE_CHOICES)
        self.assertIn(self.table.table_size, choices.keys())

    def test_unique_table_number(self):
        """Тест: номер стола уникален."""
        with self.assertRaises(Exception):
            Table.objects.create(
                table_status='Available',
                table_number=1,  # Дублируем существующий номер
                table_size='Big'
            )


class ReservationModelTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            phone='+1234567890',
            first_name="Test",
            last_name="User"
        )

        # Создаем тестовый стол
        self.table = Table.objects.create(
            table_status="Available",
            table_number=1,
            table_size="Small"
        )

        # Создаем тестовую бронь
        self.reservation = Reservation.objects.create(
            reservation_date=date.today(),
            reservation_start=time(12, 30),
            guests_amount="1-2",
            reservation_status="Активна",
            reserved_table=self.table,
            owner=self.user,
            reservation_commentary="Окно, пожалуйста"
        )

    def test_reservation_creation(self):
        """Проверяем, что бронь создается корректно"""
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(self.reservation.reserved_table, self.table)
        self.assertEqual(self.reservation.owner, self.user)
        self.assertEqual(self.reservation.reservation_status, "Активна")
        self.assertEqual(self.reservation.reservation_commentary, "Окно, пожалуйста")

    def test_reservation_number_generation(self):
        """Проверяем, что у брони генерируется уникальный номер"""
        self.assertIsNotNone(self.reservation.reservation_number)
        self.assertEqual(len(self.reservation.reservation_number), 6)

    def test_reservation_str(self):
        """Проверяем строковое представление объекта брони"""
        expected_str = (
            f"Дата брони - {self.reservation.reservation_date}, "
            f"время брони - {self.reservation.reservation_start}, "
            f"владелец брони - {self.reservation.owner},"
            f"номер брони - {self.reservation.reservation_number}"
        )
        self.assertEqual(str(self.reservation), expected_str)

    def test_update_reservation_status(self):
        """Проверяем возможность изменения статуса брони"""
        self.reservation.reservation_status = "Отменена"
        self.reservation.save()
        self.assertEqual(self.reservation.reservation_status, "Отменена")

    def test_null_reserved_table(self):
        """Проверяем, что столик можно установить в NULL"""
        self.reservation.reserved_table = None
        self.reservation.save()
        self.assertIsNone(self.reservation.reserved_table)

    def test_create_multiple_reservations(self):
        """Проверяем создание нескольких броней"""
        Reservation.objects.create(
            reservation_date=date.today(),
            reservation_start=time(15, 0),
            guests_amount="3-4",
            reservation_status="Активна",
            reserved_table=self.table,
            owner=self.user
        )
        self.assertEqual(Reservation.objects.count(), 2)

    def test_invalid_reservation_date(self):
        """Проверяем, что нельзя забронировать столик на прошедшую дату"""
        form_data = {
            'reservation_date': date.today() - timedelta(days=3),
            'reservation_start': (timezone.localtime() + timedelta(hours=2)).time(),
            'guests_amount': "1-2",
            'reservation_commentary': "Окно, пожалуйста",
        }

        form = ReservationForm(data=form_data)

        # Ожидаем, что форма не будет валидной
        self.assertFalse(form.is_valid())

    def test_invalid_reservation_time(self):
        """Проверяем, что нельзя забронировать столик на сегодня на прошедшее время"""
        form_data = {
            'reservation_date': date.today(),
            'reservation_start': (timezone.localtime() - timedelta(hours=2)).time(),
            'guests_amount': "1-2",
            'reservation_commentary': "Окно, пожалуйста",
        }

        form = ReservationForm(data=form_data)

        # Ожидаем, что форма не будет валидной
        self.assertFalse(form.is_valid())

    def test_invalid_reservation_time_working_hours(self):
        """Проверяем, что нельзя забронировать столик на нерабочие часы ресторана"""
        form_data = {
            'reservation_date': date.today(),
            'reservation_start': time(8, 30),
            'guests_amount': "1-2",
            'reservation_commentary': "Окно, пожалуйста",
        }

        form = ReservationForm(data=form_data)

        # Ожидаем, что форма не будет валидной
        self.assertFalse(form.is_valid())
