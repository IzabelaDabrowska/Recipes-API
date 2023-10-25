import random
from unittest import mock

# from django.core import mail
from django.test import TestCase

from .models import AppUser


def mock_choices(choices, k=1):
    return ["A"] * k


def mock_send_mail():
    return print('send mail')


class AppUserTestCase(TestCase):
    @mock.patch("random.choices", side_effect=mock_choices)
    def test_set_valid_activation_code(self, mock_random_choices):
        user = AppUser.objects.create(email='test@test.pl', password="admin12345")
        user.save()
        self.assertIsNone(user.activation_code)
        self.assertIsNone(user.activation_code_valid_until)
        user.set_activation_code()
        self.assertIsNotNone(user.activation_code)
        self.assertIsNotNone(user.activation_code_valid_until)
        self.assertEqual(user.activation_code, 'AAAAAAAA')
        mock_random_choices.assert_called()

    def test_register(self):
        with mock.patch("django.core.mail.send_mail") as mock_mail:
            mock_mail.side_effect = mock_send_mail
            user = AppUser.objects.create(email='test@test.pl', password="admin12345")
            user.register(password="admin12345")
            self.assertIsNotNone(user.password)
            self.assertFalse(user.is_active)
            self.assertIsNotNone(user.activation_code)
            mock_mail.assert_called()
