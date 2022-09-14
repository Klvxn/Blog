from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from .api import urls
from . import views


app_name = "users"

urlpatterns = [
    path("api/", include(urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterUser, name="register"),
]
