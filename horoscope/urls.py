from django.urls import path
from .views import horoscopos_hoy

urlpatterns = [
    path('horoscopos/', horoscopos_hoy, name='horoscopos_hoy'),
]