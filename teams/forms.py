from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget
from .models import Team
from core.models import Player


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'logo',

        ]
    #
    # def clean(self, *args, **kwargs):
    #     super().clean()
    #     """
    #     Checks that team players not more than 22 players.
    #     """
    #     players = self.cleaned_data.get('players')
    #     print(players)
    #
    #     if len(players) > 22:
    #         raise ValidationError("The Team players can not be more than 22 players")
    #     return self.cleaned_data
