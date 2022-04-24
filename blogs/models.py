from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    email = models.EmailField()
    bio = models.TextField(null=True)

    def __str__(self):
        return f'{self.firstname}'

    def get_absolute_url(self):
        return reverse("blogs:author", kwargs={"firstname": self.firstname, "lastname":self.lastname})    


class BlogPost(models.Model):
    """A post the user will post on the blog."""
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = models.SlugField(max_length=100, null = True)
    date_added = models.DateTimeField('Date Published', default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Return a string representation of the blog."""
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse("blogs:post_detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    username  = models.CharField(max_length=100)
    text = models.TextField(('Comment'), null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.text} by {self.username}'
