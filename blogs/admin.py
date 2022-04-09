from django.contrib import admin
# from django.contrib.admin.options import ModelAdmin
# from django.db.models.base import Model

from .models import BlogPost, Comment

# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'date_added')
    search_fields = ['title']

admin.site.register(Comment)