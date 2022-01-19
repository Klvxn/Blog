from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'blogs'

urlpatterns = [
    # index page.
    path('', views.IndexView.as_view(), name='index'),
    
    # new post.
    path('create_post/', views.create_post, name='create_post'),

    # edit post
    url(r'^edit_post/(?P<post_id>\d+)/$', views.edit_post, name='edit_post')

    ]
