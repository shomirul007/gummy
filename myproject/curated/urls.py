from django.urls import path
from .views import CuratedAPIView

urlpatterns = [
    path('curated/', CuratedAPIView.as_view(), name='curated-api'),
]
