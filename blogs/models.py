from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    """A post the user will post on the blog."""
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=500)
    date_added = models.DateTimeField('Date Published', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """Return a string representation of the blog."""
        return f'{self.title}'
