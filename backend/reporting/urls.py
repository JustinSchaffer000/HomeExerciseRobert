from django.urls import path, include
from .views import Custormer

urlpatterns = [
    path('', Custormer, name="cunstomer")
]
