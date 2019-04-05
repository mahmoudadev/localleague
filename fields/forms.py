from django import forms
from .models import Field, Image


class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = [
            'name',
            'description',
            'area',
            'location',

        ]



class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Image
        fields = ('image', )