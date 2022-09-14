from django.urls import path, include

from .api import urls
from .views import (author_detail, authors_list, become_author,
                    edit_author_profile, search_authors)


app_name = "authors"

urlpatterns = [
    path("authors/", authors_list, name="authors"),
    path("authors/<slug:slug>/", author_detail, name="author_detail"),
    path("authors/join/become-an-author/", become_author, name="become_author"),
    path("authors/<slug:slug>/edit-profile/", edit_author_profile, name="edit_author_profile"),
    path("search-authors/", search_authors, name="search_authors"),
    path("api/", include(urls))
]

