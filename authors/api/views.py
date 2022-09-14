from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse

from ..models import Author
from .permissions import IsUserOrReadOnly
from .serializers import AuthorSerializer


# Create your views here.

class AuthorsList(generics.ListAPIView):

    authentication_classes = [BasicAuthentication]
    lookup_field = "slug"
    queryset = Author.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [BasicAuthentication]
    lookup_field = "slug"
    queryset = Author.objects.all()
    permission_classes = (IsUserOrReadOnly | IsAdminUser,)
    serializer_class = AuthorSerializer
