from abc import ABC

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from account.forms import CategoryForm, SpendForm
from account.models import Categories


class TestsViewsContainForm(ABC):
    test_url = None
    test_form = None
    test_template = None
    permission = None
    filled_form = None

    def setUp(self):
        user_model = get_user_model()
        permission = Permission.objects.get(codename=self.permission)

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

        self.right_form = self.filled_form

    def test_get_without_user(self):
        resp = self.client.get(reverse(self.test_url))
        expected_url = f'{reverse("login")}?next={reverse(self.test_url)}'
        self.assertRedirects(
            resp, expected_url,
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=True)

    def test_get_with_wrong_user(self):
        self.client.login(
            username='user_without_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        self.assertEqual(resp.status_code, 403)

    def test_get_with_right_permission(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        self.assertEqual(resp.status_code, 200)

    def test_get_receive_form(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        form = resp.context['form']
        self.assertIsInstance(form, self.test_form)

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        self.assertTemplateUsed(resp, self.test_template)

    def test_post_right_filled_form_redirect(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(reverse(self.test_url), self.right_form)
        self.assertRedirects(
            resp, reverse('account:index'),
            status_code=302, target_status_code=403,
            msg_prefix='', fetch_redirect_response=True,
        )

    def test_post_wrong_form_resp_status_200(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(reverse(self.test_url), {})
        self.assertEquals(resp.status_code, 200)

    def test_post_wrong_form_uses_right_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(reverse(self.test_url), {})
        self.assertTemplateUsed(resp, self.test_template)

    def test_post_wrong_form_return_error(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(reverse(self.test_url), {})
        self.assertContains(resp, 'This field is required.', html=True)


class TestCreateCategory(TestsViewsContainForm, TestCase):
    test_url = 'account:create_category'
    test_form = CategoryForm
    test_template = 'account/create_category.html'
    permission = 'add_categories'
    filled_form = {'category_name': 'test_category'}


class TestCreateSpend2(TestsViewsContainForm, TestCase):
    test_url = 'account:create_spend'
    test_form = SpendForm
    test_template = 'account/create_spend.html'
    permission = 'add_spends'

    @property
    def filled_form(cls):
        category = Categories.objects.create(category_name='test_category')
        category.save()
        right_form = {
            'payer': '1',
            'category': category.id,
            'cost': 123,
            'cost_date': '2020-12-19'
        }
        return right_form
