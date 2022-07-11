from ckeditor.fields import RichTextField

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from authors.models import Author


class BlogPost(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextField(max_length=7000)
    slug = models.SlugField(max_length=200, unique=True)
    source = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField("Date Published", default=timezone.now)

    class Meta:
        ordering = ["-date_added"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blogs:post_detail", args=[self.slug, self.pk])


class Comment(models.Model):

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    text = models.TextField(("Comment"))
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text} by {self.username}"
