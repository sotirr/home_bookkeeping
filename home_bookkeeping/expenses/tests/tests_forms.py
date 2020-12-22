from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from expenses.forms import CategoryForm, SpendForm
from expenses.models import Categories, Spends


class TestSpendForm(TestCase):

    def test_clean_cost_date_date_in_future(self):
        date_in_future = timezone.now().date() + timedelta(days=1)
        form = SpendForm({'cost_date': date_in_future})
        self.assertEqual(
            form.errors['cost_date'],
            ['Data cannot be in the future']
        )

    def test_clean_cost_date_date_right_date(self):
        date = timezone.now().date()
        form = SpendForm({'cost_date': date})
        self.assertIsNone(form.errors.get('cost_date'))

    def test_clean_cost_value_under_zero(self):
        form = SpendForm({'cost': -10})
        self.assertEqual(
            form.errors['cost'],
            ['cost must be a positive number']
        )

    def test_clean_cost_positive_value(self):
        form = SpendForm({'cost': 10})
        self.assertIsNone(form.errors.get('cost'))
        SpendForm

    def test_payer_get_right_queriset(self):
        self.create_users()
        form = SpendForm()
        users = form.fields['payer'].queryset
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].username, 'user_with_permission')

    def test_save_functional(self):
        self.create_users()
        user = get_user_model().objects.get(username='user_with_permission')
        category = Categories.objects.create(category_name='test_category')
        category.save()
        bound_form = SpendForm(dict(
            payer=user.id,
            category=category.id,
            cost=123,
            cost_date='2020-12-19',
            comment='spend1',
        ))
        bound_form.is_valid()
        bound_form.save()
        self.assertIsNotNone(Spends.objects.filter(comment='spend1').first())

    def create_users(self):
        user_model = get_user_model()
        permission = Permission.objects.get(codename='add_spends')

        user_with_permission = user_model.objects.create_user(
            username='user_with_permission',
            password='test_password',
        )
        user_without_permission = user_model.objects.create_user(
            username='user_without_permission',
            password='test_password',
        )

        user_with_permission.user_permissions.add(permission)
        user_with_permission.save()
        user_without_permission.save()


class TestCategoryForm(TestCase):

    def test_clean_with_exist_category_name(self):
        Categories.objects.create(category_name='test_category')
        form = CategoryForm({'category_name': 'test_category'})
        self.assertEqual(
            form.errors['category_name'],
            ['This category has already exist']
        )

    def test_clean_cost_date_date_right_date(self):
        form = CategoryForm({'category_name': 'test_category'})
        self.assertIsNone(form.errors.get('category_name'))

    def test_save_functional(self):
        bound_form = CategoryForm({'category_name': 'test_category'})
        bound_form.is_valid()
        bound_form.save()
        qs = Categories.objects.filter(category_name='test_category').first()
        self.assertIsNotNone(qs)
