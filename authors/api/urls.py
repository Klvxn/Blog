from django.urls import path

from .views import AuthorDetail, AuthorsList


urlpatterns = [
    path("authors/", AuthorsList.as_view(), name="authors"),
    path("authors/<slug:slug>/", AuthorDetail.as_view(), name="author-detail")
]
