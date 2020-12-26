from abc import ABC

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone

from expenses.forms import CategoryForm, SpendForm
from expenses.models import Categories, Spends
from expenses.filters import CostDateFilter


class TestsPermission(ABC):
    test_url = None
    args = None
    kwargs = None
    permission = None

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

        self.url = reverse(self.test_url, args=self.args, kwargs=self.kwargs)

    def test_get_without_user(self):
        resp = self.client.get(self.url)
        expected_url = f'{reverse("login")}?next={self.url}'
        self.assertRedirects(
            resp, expected_url,
            status_code=302, target_status_code=200,
            msg_prefix='', fetch_redirect_response=True)

    def test_get_with_wrong_user(self):
        self.client.login(
            username='user_without_permission', password='test_password',
        )
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 403)

    def test_get_with_right_permission(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)


class TestsViewsContainForm(TestsPermission, ABC):
    test_form = None
    test_template = None
    filled_form = None

    def setUp(self):
        super().setUp()
        self.right_form = self.filled_form

    def test_get_receive_form(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(self.url)
        form = resp.context.get('form')
        self.assertIsInstance(form, self.test_form)

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.test_template)

    def test_post_right_filled_form_redirect(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(self.url, self.right_form)
        self.assertRedirects(
            resp, reverse('expenses:index'),
            status_code=302, target_status_code=403,
            msg_prefix='', fetch_redirect_response=True,
        )

    def test_post_wrong_form_resp_status_200(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(self.url, {})
        self.assertEquals(resp.status_code, 200)

    def test_post_wrong_form_uses_right_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(self.url, {})
        self.assertTemplateUsed(resp, self.test_template)

    def test_post_wrong_form_return_error(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(self.url, {})
        self.assertContains(resp, 'This field is required.', html=True)


class TestCreateCategory(TestsViewsContainForm, TestCase):
    test_url = 'expenses:create_category'
    test_form = CategoryForm
    test_template = 'expenses/create_category.html'
    permission = 'add_categories'
    filled_form = {'category_name': 'test_category'}


class TestCreateSpend(TestsViewsContainForm, TestCase):
    test_url = 'expenses:create_spend'
    test_form = SpendForm
    test_template = 'expenses/create_spend.html'
    permission = 'add_spends'

    @property
    def filled_form(self):
        user = get_user_model().objects.get(username='user_with_permission')
        category = Categories.objects.create(category_name='test_category')
        category.save()
        right_form = {
            'payer': user.id,
            'category': category.id,
            'cost': 123,
            'cost_date': '2020-12-19'
        }
        return right_form


class TestIndex(TestsPermission, TestCase):
    test_url = 'expenses:index'
    test_template = 'expenses/index.html'
    permission = 'view_spends'
    form = CostDateFilter

    def setUp(self):
        super().setUp()
        user = get_user_model().objects.get(username='user_with_permission')
        spend1 = Spends(payer_id=user.id, cost=1,
                        cost_date=timezone.now(), comment='spend1')
        spend2 = Spends(payer_id=user.id, cost=2,
                        cost_date=timezone.now(), comment='spend2')
        spend1.save()
        spend2.save()

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        self.assertTemplateUsed(resp, self.test_template)

    def test_get_receive_filter(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        form = resp.context['filtered_data']
        self.assertIsInstance(form, self.form)

    def test_get_receive_sum_context(self):

        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        self.assertEqual(resp.context['sum'], 3)

    def test_get_receive_queryset(self):

        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url))
        receive_queryset = resp.context['object_list']
        expected_queryset = Spends.objects.all()
        self.assertQuerysetEqual(receive_queryset, expected_queryset,
                                 transform=lambda x: x)

    def test_get_params(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(reverse(self.test_url), {'comment': 'spend1'})

        receive_queryset = resp.context['object_list']
        expected_queryset = Spends.objects.filter(comment__icontains='spend1')

        self.assertQuerysetEqual(receive_queryset, expected_queryset,
                                 transform=lambda x: x)


class TestDeleteSpendView(TestsPermission, TestCase):
    test_url = 'expenses:delete_spend'
    permission = 'delete_spends'
    test_template = 'expenses/delete_spend.html'

    @property
    def kwargs(self):
        user = get_user_model().objects.get(
            username='user_with_permission'
        )
        user2 = get_user_model().objects.get(
            username='user_without_permission'
        )
        spend1 = Spends(payer_id=user.id, cost=1,
                        cost_date=timezone.now(), comment='spend1')
        self.spend2 = Spends(payer_id=user2.id, cost=1,
                             cost_date=timezone.now(), comment='spend2')
        spend1.save()
        self.spend2.save()
        return {'pk': spend1.pk}

    def test_uses_correct_template(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(self.url)
        self.assertTemplateUsed(resp, self.test_template)

    def test_post_right_redirect(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(self.url)
        self.assertRedirects(
            resp, reverse('expenses:index'),
            status_code=302, target_status_code=403,
            msg_prefix='', fetch_redirect_response=True,
        )

    def test_get_attempt_delete_not_own_spend_status_code(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(
            reverse(self.test_url, kwargs={'pk': self.spend2.pk})
        )
        self.assertEqual(resp.status_code, 403)

    def test_post_attempt_delete_not_own_spend_status_code(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse(self.test_url, kwargs={'pk': self.spend2.pk})
        )
        self.assertEqual(resp.status_code, 403)

    def test_get_attempt_delete_not_own_spend_msg(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.get(
            reverse(self.test_url, kwargs={'pk': self.spend2.pk})
        )
        self.assertContains(
            resp, '<h1>You can delete only own spends<h1>',
            html=True, status_code=403,
        )

    def test_post_attempt_delete_not_own_spend_msg(self):
        self.client.login(
            username='user_with_permission', password='test_password',
        )
        resp = self.client.post(
            reverse(self.test_url, kwargs={'pk': self.spend2.pk})
        )
        self.assertContains(
            resp, '<h1>You can delete only own spends<h1>',
            html=True, status_code=403,
        )
