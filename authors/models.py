from ckeditor.fields import RichTextField
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(("First Name"), max_length=10)
    last_name = models.CharField(("Last Name"), max_length=10)
    image = models.ImageField(("Profile Picture"), upload_to="media/avis/", null=True)
    slug = models.SlugField(unique=True)
    email = models.EmailField(("Email Address"), unique=True)
    bio = RichTextField(("About yourself"))
    date_joined = models.DateField(auto_now_add=True, null=True)

    class Meta:
        ordering = ("-date_joined",)

    def joined_recently(self):
        now = timezone.now().date()
        if now - self.date_joined < timedelta(days=5):
            return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("authors:author_detail", args=[self.slug])
