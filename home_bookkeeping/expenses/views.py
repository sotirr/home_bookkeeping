from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import ListView, View
from django.db.models import Sum
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Spends
from .forms import SpendForm, CategoryForm
from .filters import CostDateFilter


class Index(PermissionRequiredMixin, ListView):
    model = Spends
    template_name = 'expenses/index.html'
    permission_required = 'expenses.view_spends'

    def get_queryset(self):
        qs = self.model.objects.all()
        self.filtered_list = CostDateFilter(self.request.GET, queryset=qs)
        return self.filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_data'] = self.filtered_list
        context['sum'] = self.filtered_list.qs.aggregate(Sum('cost'))['cost__sum']
        return context


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
        else:
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
        else:
            return render(request, 'expenses/create_category.html',
                          context={'form': bound_form})
