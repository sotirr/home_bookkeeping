from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView, PasswordResetConfirmView
)
from django.urls import reverse_lazy

from . import forms


# Create your views here.
class SignUpView(CreateView):
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    form_class = forms.CustomAuthForm
    extra_context = {'title': 'Login'}


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = forms.CustomPasswordResetForm
