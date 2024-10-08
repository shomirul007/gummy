from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/subreddit/', include('subreddit.urls')),
    path('api/', include('curated.urls')),
    path('api/', include('posts.urls')),
    path('reddit/', include('reddit_analysis.urls')),
]
