from django.db import models
from home.models import UserProfile
from django.contrib import admin
from PIL import Image

from django.utils.safestring import mark_safe 

# Create your models here.

class Article(models.Model):
  
  title = models.CharField(max_length=120)
  body = models.TextField()
  image = models.FileField(upload_to ="static/pictures/id/%Y/%m/", null=True, blank=True)
  owner = models.ForeignKey(UserProfile)
  is_project = models.BooleanField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)

  def display_safe_body(self): 
      return mark_safe(self.body)

  def display_safe_title(self): 
      return mark_safe(self.title)
  
  def __unicode__(self):
    return self.title
