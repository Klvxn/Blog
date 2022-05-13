from django.urls import path

from . import views


app_name = 'blogs'

urlpatterns = [
    # Home page.
    path('', views.IndexView, name='index'),
    # Post detail
    path('post/<slug:slug>/<int:pk>/', views.PostDetail, name='post_detail'),
    # Create post.
    path('create-post/', views.create_post, name='create_post'),
    # Edit post
    path('post/<slug:slug>/<int:pk>/edit-post/', views.edit_post, name='edit_post'),
    # Delete post
    path('post/<slug:slug>/<int:pk>/delete-post/', views.delete_post, name='delete_post'),
    # Authors page
    path('authors/', views.authors, name='authors'),
    # Author page
    path('author/<slug:firstname>-<slug:lastname>/', views.author, name='author'),
    path('become-an-author/', views.beauthor, name='beauthor'),
    path('author/<slug:firstname>-<slug:lastname>/edit-profile/', views.edit_author_profile, name='edit_author_profile'),
    # Search page
    path('search/', views.search, name='search'),
    ]
