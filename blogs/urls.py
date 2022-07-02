from django.urls import path

from . import views


app_name = "blogs"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("posts/<slug:slug>/<int:pk>/", views.post_detail, name="post_detail"),
    path("create-post/", views.create_post, name="create_post"),
    path("posts/<slug:slug>/<int:pk>/edit-post/", views.edit_post, name="edit_post"),
    path("posts/<slug:slug>/<int:pk>/delete-post/", views.delete_post, name="delete_post"),
    path("search-posts/", views.search_posts, name="search_posts"),
]


