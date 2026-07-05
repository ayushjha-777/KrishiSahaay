from django.urls import path
from .views import HealthCheckView, PredictAPIView

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health"),
    path("predict/", PredictAPIView.as_view(), name="predict"),
    
]