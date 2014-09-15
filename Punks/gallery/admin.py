from django.contrib import admin
from gallery.models import Artwork
from gallery.models import Category

# Register your models here.
class GalleryAdmin(admin.ModelAdmin):
  list_display = ("title", "owner","pk")
  
admin.site.register(Artwork)
admin.site.register(Category, GalleryAdmin)
