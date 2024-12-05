from django.test import TestCase
from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import PhoneNumber
from django.db import IntegrityError
from users.models import User, Feedback


class UserModelTest(TestCase):

    def setUp(self):
        """Создаем тестового пользователя для использования в тестах"""
        self.user_data = {
            'email': 'testuser@example.com',
            'phone': PhoneNumber.from_string('+1234567890'),
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """Проверяем создание пользователя"""
        user = self.user
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.phone, self.user_data['phone'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_unique_email(self):
        """Проверяем уникальность поля email"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='testuser@example.com',
                                     phone='+1987654321', first_name='Another',
                                     last_name='User')

    def test_unique_phone(self):
        """Проверяем уникальность поля phone"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='newuser@example.com',
                                     phone='+1234567890', first_name='New',
                                     last_name='User')

    def test_str_method(self):
        """Проверяем корректность метода __str__"""
        self.assertEqual(str(self.user), self.user_data['email'])


class FeedbackModelTest(TestCase):

    def setUp(self):
        """Создаем тестовую запись обратной связи"""
        self.feedback_data = {
            'name': 'John Doe',
            'phone': '+1234567890',
            'message': 'This is a test message.'
        }
        self.feedback = Feedback.objects.create(**self.feedback_data)

    def test_feedback_creation(self):
        """Проверяем создание записи обратной связи"""
        feedback = self.feedback
        self.assertEqual(feedback.name, self.feedback_data['name'])
        self.assertEqual(feedback.phone, self.feedback_data['phone'])
        self.assertEqual(feedback.message, self.feedback_data['message'])

    def test_feedback_str_method(self):
        """Проверяем корректность метода __str__"""
        expected_str = (f'Обратная связь от {self.feedback_data["name"]} '
                        f'({self.feedback_data["phone"]}):\n{self.feedback_data["message"]}')
        self.assertEqual(str(self.feedback), expected_str)

    def test_feedback_validation(self):
        """Проверяем валидацию на пустые поля"""
        invalid_feedback_data = {
            'name': '',
            'phone': '',
            'message': ''
        }
        with self.assertRaises(ValidationError):
            invalid_feedback = Feedback(**invalid_feedback_data)
            invalid_feedback.full_clean()  # Вызывает валидацию
