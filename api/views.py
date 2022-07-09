from django.contrib.auth.models import User

from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from authors.models import Author
from blogs.models import BlogPost

from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly
from .serializers import AuthorSerializer, BlogSerializer, UserSerializer


# Create your views here.
@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "Blog List": reverse("api:blogs", request=request, format=format),
            "Author List": reverse("api:authors", request=request, format=format),
            "Users List": reverse("api:users", request=request, format=format),
        }
    )


class BaseView(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, args, kwargs)


class BlogList(ListAPIView):

    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(BaseView):

    permission_classes = (IsAuthorOrReadOnly | IsAdminUser,)
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer


class AuthorsList(ListAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(BaseView):

    permission_classes = (IsUserOrReadOnly | IsAdminUser,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class UserList(ListAPIView):

    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(BaseView):

    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
