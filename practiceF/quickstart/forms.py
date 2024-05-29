from .models import user_image
from django.forms import ModelForm
from django import forms

class user_image_form(ModelForm):

    class Meta:
        model = user_image
        fields = ['title','username','image_downloaded']

""" class user_image_downloaded(forms.Form):
    title = forms.CharField()
    image_downloaded = forms.ImageField() """