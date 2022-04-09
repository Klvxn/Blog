from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blogs'

urlpatterns = [
    # index page.
    path('', views.IndexView, name='index'),

    # post detail
    path('posts/<int:pk>/', views.PostDetail, name='post_detail'),
    
    # new post.
    path('create-post/', views.create_post, name='create_post'),

    # edit post
    path('posts/<int:post_id>/edit-post/', views.edit_post, name='edit_post'),

    # delete post
    path('posts/<int:post_id>/delete-post/', views.delete_post, name='delete_post'),

    # post a comment 
    #path('posts/<int:post_id>/post-comment/', views.comment, name='post-comment'),

    # Login redirect page
    path('registration/login/', auth_views.LoginView.as_view()),


    ]
