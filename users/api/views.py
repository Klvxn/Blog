from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import UserSerializer, UserRegisterSerializer


class UserList(generics.ListAPIView):

    authentication_classes = [BasicAuthentication]
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegister(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
