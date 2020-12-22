from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from accounts.forms import CustomUserCreationForm


class TestCustomUserCreationForm(TestCase):

    def test_clean_email_with_duplicate_email(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='test_user',
            password='test_password',
            email='name@example.com',
        )
        form = CustomUserCreationForm({'email': 'name@example.com'})
        self.assertEqual(
            form.errors['email'],
            ['Such email is already used'],
        )

    def test_clean_email_with_uniq_email(self):
        form = CustomUserCreationForm({'email': 'name@example.com'})
        self.assertIsNone(form.errors.get('email'))

    def test_save_functional(self):
        payer_group = Group(name='Payers')
        payer_group.save()
        user_model = get_user_model()
        bound_form = CustomUserCreationForm({
            'username': 'test_user',
            'password1': 'test_password',
            'password2': 'test_password',
            'email': 'name@example.com',
        })
        bound_form.is_valid()
        bound_form.save()
        qs = user_model.objects.filter(username='test_user').first()
        self.assertIsNotNone(qs, msg='form was not saved id db')
