from django.contrib import admin
# from django.contrib.admin.options import ModelAdmin
# from django.db.models.base import Model

from .models import BlogPost

# Register your models here.
admin.site.register(BlogPost)