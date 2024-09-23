from django.urls import path
from .views import SentimentAnalysisAPIView

urlpatterns = [
    path('analyze-sentiments/', SentimentAnalysisAPIView.as_view(), name='analyze_sentiments'),
]