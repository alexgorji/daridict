from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from accounts.forms import UserRegistrationForm, MyAuthenticationForm

User = get_user_model()


class TestUserRegistrationForm(TestCase):
    def setUp(self) -> None:
        self.testuserdata = {'username': 'testuser', 'password': '1234', 'password2': '1234', 'email': 'a@b.com'}

    def test_user_registration_form_fields(self):
        form = UserRegistrationForm(data=self.testuserdata)
        form.save()
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')

    def test_password2(self):
        form = UserRegistrationForm(data=self.testuserdata)
        form.save()
        cd = form.cleaned_data
        self.assertEqual(cd, self.testuserdata)

    def test_user_password_repeat(self):
        form = UserRegistrationForm(
            data={'username': 'testuser', 'password': '1234', 'password2': '4321', 'email': 'a@b.com',
                  'first_name': 'Alfred', 'last_name': 'Tester'})
        self.assertFalse(form.is_valid())
        self.assertTrue(isinstance(form.errors.as_data()['password2'][0], ValidationError))
        with self.assertRaises(ValueError):
            form.save()

    def test_user_model_is_saved(self):
        form = UserRegistrationForm(data=self.testuserdata)
        self.assertTrue(form.is_valid())
        user = form.save()
        user_query = User.objects.get(username='testuser')
        self.assertEqual(user, user_query)

    def test_required_fields(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        for key in ['username', 'password', 'password2', 'email']:
            self.assertTrue(key in form.errors.as_data().keys())


class TestMyAuthenticationForm(TestCase):
    def setUp(self) -> None:
        self.user_data = {'username': 'tester', 'password': '1234', 'email': 'tester@tester.com'}
        self.user = User.objects.create_user(**self.user_data)

    def test_required_fields(self):
        form = MyAuthenticationForm(data={})
        self.assertFalse(form.is_valid())
        for key in ['username', 'password']:
            self.assertTrue(key in form.errors.as_data().keys())

    def test_valid_user_name_and_password(self):
        form = MyAuthenticationForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_invalid_user_name_or_password(self):
        data = {**self.user_data}
        data['username'] = 'newtester'
        form = MyAuthenticationForm(data=data)
        form.full_clean()
        self.assertFalse(form.is_valid())
        # print(form.errors.as_data())
        self.assertTrue(isinstance(form.errors.as_data()['__all__'][0], ValidationError))
