from django.urls import path

from .views import UserDetail, UserList, UserRegister

urlpatterns = [
    path("users/", UserList.as_view(), name="users"),
    path("r/", UserRegister.as_view()),
    path("users/<int:pk>/", UserDetail.as_view(), name="user-detail"),
]
