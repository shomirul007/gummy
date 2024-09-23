from django.urls import path
from .views import PostsAPIView
from . import views

urlpatterns = [
    path('posts/', PostsAPIView.as_view(), name='posts-api'),
]
