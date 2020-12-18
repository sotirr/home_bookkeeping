from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from account.models import Spends, Categories


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.category = Categories.objects.create(
            category_name='Test_category'
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Test_category')

    def test_category_get_absolute_url(self):
        absolute_url = self.category.get_absolute_url()
        self.assertEqual(absolute_url, '/account/')


class TestSpendsModel(TestCase):

    def setUp(self):
        category = Categories.objects.create(
            category_name='test_category'
        )
        user_model = get_user_model()
        payer = user_model.objects.create(username='test_payer')
        self.spend = Spends.objects.create(
            payer=payer, category=category, cost=10.1, cost_date=timezone.now(),
        )

    def test_spend_creation(self):
        self.assertEqual(
            str(self.spend),
            'test_payer, test_category, 10.1, '
        )

    def test_spend_get_absolute_url(self):
        absolute_url = self.spend.get_absolute_url()
        self.assertEqual(absolute_url, '/account/')