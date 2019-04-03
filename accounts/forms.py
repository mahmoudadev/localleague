from django import forms
from core.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistraionForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'user_type',
            'username',
            'first_name',
            'last_name',
            'email'
        ]
