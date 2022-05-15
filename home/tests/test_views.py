from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from helpers.functions import create_profile
from helpers.variables import norman_data

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self) -> None:
        self.norman = create_profile(norman_data)
        super().setUp()

    def test_status_code_not_signed(self):
        """
        Test home returns a response with status_code 302
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(reverse('profiles_login') + '?next=/', response['location'])

    def test_status_code_signed(self):
        """
        Test home returns a response with status_code 302
        """
        self.client.force_login(self.norman.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        """
        Test that home view redirects to tax return list
        """
        self.client.force_login(self.norman.user)
        response = self.client.get('/')
        self.assertEqual(302, response.status_code)
        self.assertEqual(reverse('taxreturns_list', kwargs={'owner_pk': self.norman.pk}), response['Location'])
