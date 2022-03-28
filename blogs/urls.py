from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'blogs'

urlpatterns = [
    # index page.
    path('', views.IndexView.as_view(), name='index'),
    
    # new post.
    path('create_post/', views.create_post, name='create_post'),

    # edit post
    path('<int:post_id>/edit_post/', views.edit_post, name='edit_post'),

    # delete post
    path('<int:post_id>/delete_post/', views.delete_post, name='delete_post'),

    # Login redirect page
    path('registration/login/', auth_views.LoginView.as_view()),


    ]
