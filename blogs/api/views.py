from django.utils.text import slugify

from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from ..models import BlogPost
from .permissions import IsAuthorOrReadOnly
from .serializers import BlogSerializer


class BlogList(generics.ListCreateAPIView):

    authentication_classes = [BasicAuthentication]
    lookup_field = "slug"
    queryset = BlogPost.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser)
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [BasicAuthentication]
    lookup_field = "slug"
    queryset = BlogPost.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminUser, IsAuthenticatedOrReadOnly)
    serializer_class = BlogSerializer

    def perform_update(self, serializer):
        serializer.validated_data["slug"] = slugify(serializer.validated_data["title"])
        return super().perform_update(serializer)
