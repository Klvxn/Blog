from django.contrib import admin

from .models import Author


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_joined")
    prepopulated_fields = {"slug": ("first_name", "last_name")}


admin.site.register(Author, AuthorAdmin)
