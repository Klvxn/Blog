from django.urls import path

from . import views

app_name = "authors"

urlpatterns = [
    path("", views.authors, name="authors"),
    path("<slug:slug>/", views.author_detail, name="author-detail"),
    path("join/become-an-author/", views.become_author, name="become-author"),
    path("<slug:slug>/edit-profile/", views.edit_author_profile, name="edit_author_profile"),
]
