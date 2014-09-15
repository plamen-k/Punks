from django.forms import ModelForm
from article.models import Article
from django import forms

class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('owner','is_project')  
    