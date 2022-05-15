from unittest import TestCase

from django.urls import resolve

class TestHomeUrls(TestCase):
    def test_home_url(self):
        match = resolve('/')
        self.assertEqual(match.view_name, 'home')
