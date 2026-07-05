from django.urls import path
from .views import PredictAPIView, HealthCheckView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health"),
    path("predict/", PredictAPIView.as_view(), name="predict"),
]