from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import Spends, Categories


class SpendForm(forms.Form):
    payer = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(
            Q(groups__permissions__codename='add_spends') |
            Q(user_permissions__codename='add_spends')
        ),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    comment = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    cost = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    cost_date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean_cost_date(self):
        date = self.cleaned_data['cost_date']
        if date > timezone.now().date():
            raise ValidationError("Data cannot be in the future")
        return date

    def clean_cost(self):
        clean_cost = self.cleaned_data['cost']
        if clean_cost < 0:
            raise ValidationError('cost must be a positive number')
        return clean_cost

    def save(self):
        new_spend = Spends.objects.create(**self.cleaned_data)
        return new_spend


class CategoryForm(forms.Form):
    category_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_category_name(self):
        clean_name = self.cleaned_data['category_name']
        duplicate_names = Categories.objects.filter(category_name=clean_name)
        if duplicate_names.count():
            raise ValidationError('This category has already exist')
        return clean_name

    def save(self):
        new_category = Categories.objects.create(**self.cleaned_data)
        return new_category
