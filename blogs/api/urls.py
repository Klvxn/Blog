from django.urls import path

from .views import BlogDetail, BlogList

app_name = "api"

urlpatterns = [
    path("posts/", BlogList.as_view(), name="blogs"),
    path("posts/<slug:slug>/", BlogDetail.as_view(), name="blog-detail"),
]
