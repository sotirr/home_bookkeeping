from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, View, DeleteView
from django.db.models import Sum
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.defaults import permission_denied

from .models import Spends
from .forms import SpendForm, CategoryForm
from .filters import CostDateFilter


class Index(PermissionRequiredMixin, ListView):
    permission_required = 'expenses.view_spends'

    model = Spends
    paginate_by = 3
    template_name = 'expenses/index.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        self.filtered_list = CostDateFilter(self.request.GET, queryset=qs)
        return self.filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_data'] = self.filtered_list
        context['sum'] = self._count_sum()
        context['saved_params'] = self._save_get_params()
        return context

    def _save_get_params(self) -> str:
        get_copy = self.request.GET.copy()
        if get_copy.get('page'):
            get_copy.pop('page')
        return get_copy.urlencode()

    def _count_sum(self) -> int:
        return self.filtered_list.qs.aggregate(Sum('cost'))['cost__sum']


class CreateSpend(PermissionRequiredMixin, View):
    permission_required = 'expenses.add_spends'

    def get(self, request):
        form = SpendForm()
        return render(request, 'expenses/create_spend.html',
                      context={'form': form})

    def post(self, request):
        bound_form = SpendForm(request.POST)
        if bound_form.is_valid():
            new_spend = bound_form.save()
            return redirect(new_spend)

        return render(request, 'expenses/create_spend.html',
                      context={'form': bound_form})


class CreateCategory(PermissionRequiredMixin, View):
    permission_required: str = 'expenses.add_categories'

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm()
        return render(request, 'expenses/create_category.html',
                      context={'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        bound_form = CategoryForm(request.POST)
        if bound_form.is_valid():
            new_category = bound_form.save()
            return redirect(new_category)

        return render(request, 'expenses/create_category.html',
                      context={'form': bound_form})


class DeleteSpend(PermissionRequiredMixin, DeleteView):
    permission_required: str = 'expenses.delete_spends'

    model = Spends
    success_url = reverse_lazy('expenses:index')
    template_name = 'expenses/delete_spend.html'

    def get(self, request, *args, **kwargs):
        current_spend = self.get_object()
        if self.request.user != current_spend.payer:
            return permission_denied(
                request, 403,
                template_name='custom_errors/403_when_del_spend.html',
            )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        current_spend = self.get_object()
        if self.request.user != current_spend.payer:
            return permission_denied(
                request, 403,
                template_name='custom_errors/403_when_del_spend.html',
            )
        return super().post(request, *args, **kwargs)
