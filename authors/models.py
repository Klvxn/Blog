from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.
class Author(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(("First Name"), max_length=10)
    last_name = models.CharField(("Last Name"), max_length=10)
    image = models.ImageField(("Profile Picture"), upload_to="media/avis/", null=True)
    slug = models.SlugField(unique=True)
    email = models.EmailField(("Email Address"), unique=True)
    bio = models.TextField(("About yourself"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("authors:author_detail", args=[self.slug])
