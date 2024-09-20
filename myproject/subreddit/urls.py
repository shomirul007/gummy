from django.urls import path
from .views import SubredditAutocomplete, SubredditAbout

urlpatterns = [
    path('autocomplete/<str:keyword>/', SubredditAutocomplete.as_view(), name='subreddit-autocomplete'),
    path('about/<str:subreddit_name>/', SubredditAbout.as_view(), name='subreddit-about'),
]
