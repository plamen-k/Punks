from django.forms import ModelForm
from article.models import UserProfile
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)  
    