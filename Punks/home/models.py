from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.safestring import mark_safe

# Create your models here.

class UserProfile(models.Model):
  user = models.OneToOneField(User, unique=True)
  firstname = models.CharField(max_length=120)
  lastname = models.CharField(max_length=120)
  email = models.CharField(max_length=120)
  image = models.ImageField(upload_to ="static/pictures/id/%Y/%m/", null=True, blank=True, default='static/images/image.jpg')
  coverPhoto = models.ImageField(upload_to ="static/pictures/id/%Y/%m/", null=True, blank=True, default='static/images/cover.png')
  description = models.TextField()
  key_skills = models.TextField()

  def __unicode__(self):
    return self.user.username

  def display_safe_description(self):
    return mark_safe(self.description)


