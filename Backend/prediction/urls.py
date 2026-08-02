from django.urls import path
from .views import (
    HealthCheckView,
    PredictAPIView,
    RecommendationAPIView,
)

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health"),
    path("predict/", PredictAPIView.as_view(), name="predict"),
    path(
    "recommend/",
    RecommendationAPIView.as_view(),
    name="recommend"
),
]