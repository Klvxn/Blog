from django.urls import path

from . import views


app_name = "authors"

urlpatterns = [
    path("authors/", views.authors_list, name="authors"),
    path("authors/<slug:slug>/", views.author_detail, name="author_detail"),
    path("authors/join/become-an-author/", views.become_author, name="become_author"),
    path("authors/<slug:slug>/edit-profile/", views.edit_author_profile, name="edit_author_profile"),
    path("search-authors/", views.search_authors, name="search_authors")
]
