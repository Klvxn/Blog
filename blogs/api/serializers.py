from rest_framework import serializers

from authors.api.serializers import AuthorSerializer

from ..models import BlogPost


class BlogSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ("title", "slug", "text", "source", "author")
