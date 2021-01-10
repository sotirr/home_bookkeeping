from django import forms
import django_filters

from .models import Spends, Categories


class CostDateFilter(django_filters.FilterSet):
    '''
    Filtering spend records
    '''
    start_date = django_filters.DateFilter(
        field_name='cost_date',
        lookup_expr='gte',
        label='Start Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name='cost_date',
        lookup_expr='lte',
        label='End Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    payer = django_filters.ModelChoiceFilter(
        label='Payer',
        queryset=Spends.payer.get_queryset().filter(groups__name='Payers'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = django_filters.ModelChoiceFilter(
        label='Category',
        queryset=Categories.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    comment = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='comment',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
