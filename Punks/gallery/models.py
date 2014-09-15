from django.db import models
from PIL import Image
from home.models import UserProfile

# Create your models here.
class Category(models.Model):
  title = models.CharField(max_length=120)
  owner = models.ForeignKey(UserProfile)
  thumbnail = models.FileField(upload_to ="static/pictures/id/%Y/%m/", null=True, blank=True)

  def __unicode__(self):
    return self.title

class Artwork(models.Model):
  title = models.CharField(max_length=120)
  url_path = models.FileField(upload_to ="static/pictures/id/%Y/%m/", null=True, blank=True)
  
  category = models.ForeignKey(Category)
  owner = models.ForeignKey(UserProfile)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.title

