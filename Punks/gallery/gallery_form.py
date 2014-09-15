from django.forms import ModelForm
from gallery.models import Artwork, Category
from django import forms

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    exclude = ('owner',) 

class ArtworkForm(forms.ModelForm):
  class Meta:
    model = Artwork
    exclude = ('owner','category')  
    