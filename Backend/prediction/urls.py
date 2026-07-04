from django.urls import path
from.views import predictAPIView

urlpatterns = [
    
    path("predict/", predictAPIView.as_view(), name="predict"),

]