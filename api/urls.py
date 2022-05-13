from django.urls import path

from .views import *


app_name = 'api'

urlpatterns = [
    path('', api_root),
    path('blogs/', BlogList.as_view(), name='blogs'),
    path('blogs/<int:pk>/', BlogDetail.as_view(), name='blog-detail'),
    path('authors/', AuthorsList.as_view(), name='authors'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author-detail'),
    path('users/', UserList.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail')
]
