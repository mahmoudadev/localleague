from django import forms
from core.models import User, Player, Sponsor
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


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'photo',
            'date_of_birth',
            'phone',
            'city',
            'dist',
            'street',
            'bank_account',
            'paypal_account'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
        }



class UserPlayerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'photo',
            'date_of_birth',
            'phone',
            'city',
            'dist',
            'street',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
        }


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'position',
        ]



class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = [
            'business',
            'commercial_register_number',
            'logo'
        ]
