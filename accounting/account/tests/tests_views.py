from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from account.forms import CategoryForm, SpendForm
from account.models import Categories, Spends


class TestCreateSpend(TestCase):

    def setUp(self):
        user_model = get_user_model()
        permission = Permission.objects.get(codename='add_spends')

        user_without_permission = user_model.objects.create_user(
            username='user_without_permission',
            password='test_password',
        )
        user_with_permission = user_model.objects.create_user(
            username='user_with_permission',
            password='test_password',
        )

        user_with_permission.user_permissions.add(permission)
        user_with_permission.groups
        user_with_permission.save()
        user_without_permission.save()

        category = Categories.objects.create(category_name='test_category')
        category.save()

        self.right_form = {
            'payer': user_with_permission.id,
            'category': category.id,
            'cost': 123,
            'cost_date': '2020-12-19'
        }

        self.wrong_form = {
            'payer': user_with_permission,
            'category': category,
            'cost': 123,
            'cost_date': ''
        }

    def test_get_without_user(self):
        resp = self.client.get(reverse('account:create_spend'))
        expected_url = '/accounts/login/?next=/account/create_spend/'
        self.assertRedirects(
            resp, expected_url,
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=True)

    def test_get_with_wrong_user(self):
        self.client.login(
            username='user_without_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_spend'))
        self.assertEqual(resp.status_code, 403)

    def test_get_with_right_permission(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_spend'))
        self.assertEqual(resp.status_code, 200)

    def test_get_receive_form(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_spend'))
        form = resp.context['form']
        self.assertIsInstance(form, SpendForm)

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_spend'))
        self.assertTemplateUsed(resp, 'account/create_spend.html')

    def test_post_right_filled_form_redirect(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_spend'),
            self.right_form,
        )
        self.assertRedirects(
            resp, reverse('account:index'),
            status_code=302, target_status_code=403,
            msg_prefix='', fetch_redirect_response=True,
        )

    def test_post_right_filled_form_save(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_spend'),
            self.right_form,
        )
        new_spend = Spends.objects.filter(
            cost_date=self.right_form['cost_date']
        ).first()
        self.assertTrue(new_spend)

    def test_post_wrong_form_resp_status_200(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_spend'),
            self.wrong_form,
        )
        self.assertEquals(resp.status_code, 200)

    def test_post_wrong_form_uses_right_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_spend'),
            self.wrong_form,
        )
        self.assertTemplateUsed(resp, 'account/create_spend.html')

    def test_post_wrong_form_return_error(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_spend'),
            self.wrong_form,
        )
        self.assertFormError(resp, 'form', 'cost_date',
                             'This field is required.')


class TestCreateCategory(TestCase):

    def setUp(self):
        user_model = get_user_model()
        permission = Permission.objects.get(codename='add_categories')

        user_without_permission = user_model.objects.create_user(
            username='user_without_permission',
            password='test_password',
        )
        user_with_permission = user_model.objects.create_user(
            username='user_with_permission',
            password='test_password',
        )

        user_with_permission.user_permissions.add(permission)
        user_with_permission.save()
        user_without_permission.save()

    def test_get_without_user(self):
        resp = self.client.get(reverse('account:create_category'))
        expected_url = '/accounts/login/?next=/account/create_category/'
        self.assertRedirects(
            resp, expected_url,
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=True)

    def test_get_with_wrong_user(self):
        self.client.login(
            username='user_without_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_category'))
        self.assertEqual(resp.status_code, 403)

    def test_get_with_right_permission(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_category'))
        self.assertEqual(resp.status_code, 200)

    def test_get_receive_form(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_category'))
        form = resp.context['form']
        self.assertIsInstance(form, CategoryForm)

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse('account:create_category'))
        self.assertTemplateUsed(resp, 'account/create_category.html')

    def test_post_right_filled_form_redirect(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_category'),
            {'category_name': 'test_category'},
        )
        self.assertRedirects(
            resp, reverse('account:index'),
            status_code=302, target_status_code=403,
            msg_prefix='', fetch_redirect_response=True,
        )

    def test_post_right_filled_form_save(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_category'),
            {'category_name': 'test_category'},
        )
        new_category = Categories.objects.filter(
            category_name='test_category'
        ).first()
        self.assertTrue(new_category)

    def test_post_wrong_form_resp_status_200(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_category'),
            {'category_name': ''},
        )
        self.assertEquals(resp.status_code, 200)

    def test_post_wrong_form_uses_right_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_category'),
            {'category_name': ''},
        )
        self.assertTemplateUsed(resp, 'account/create_category.html')

    def test_post_wrong_form_return_error(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse('account:create_category'),
            {'category_name': ''},
        )
        self.assertFormError(resp, 'form', 'category_name',
                             'This field is required.')
