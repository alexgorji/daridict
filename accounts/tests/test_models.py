from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from django.db.utils import IntegrityError

User = get_user_model()


class TestUserModel(TestCase):
    def test_unique_username(self):
        """
        Test that user must have a unique username
        """
        data1 = {'username': 'testuser', 'password': '1234', 'email': 'a@b.com'}
        data2 = {'username': 'testuser', 'password': '1234', 'email': 'b@c.com'}
        self.user1 = User.objects.create_user(**data1)
        with self.assertRaises(IntegrityError):
            self.user2 = User.objects.create_user(**data2)

    def test_unique_email(self):
        """
        Test that user must have a unique email address
        """
        data1 = {'username': 'testuser1', 'password': '1234', 'email': 'a@b.com'}
        data2 = {'username': 'testuser2', 'password': '1234', 'email': 'a@b.com'}
        self.user1 = User.objects.create_user(**data1)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**data2)
