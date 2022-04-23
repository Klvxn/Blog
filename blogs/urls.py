import re
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blogs'

urlpatterns = [
    # index page.
    path('', views.IndexView, name='index'),
    # post detail
    path('post/<slug:slug>/', views.PostDetail, name='post_detail'),
    # new post.
    path('create-post/', views.create_post, name='create_post'),
    # edit post
    path('post/<slug:slug>/edit-post/', views.edit_post, name='edit_post'),
    # delete post
    path('post/<slug:slug>/delete-post/', views.delete_post, name='delete_post'),
    # authors page
    path('authors/', views.authors, name='authors'),
    # author page
    path('author/<slug:firstname>-<slug:lastname>/', views.author, name='author'),
    path('become-an-author/', views.beauthor, name='beauthor'),
    # search page
    path('search/', views.search, name='search'),


    # Login redirect page
    path('registration/login/', auth_views.LoginView.as_view()),
    ]
