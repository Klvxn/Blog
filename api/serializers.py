from rest_framework import serializers

from django.contrib.auth.models import User

from blogs.models import BlogPost
from authors.models import Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "is_staff",
            "is_superuser",
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "user")


class BlogSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ("id", "title", "text", "source", "author")
