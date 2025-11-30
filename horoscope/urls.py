from django.urls import path
from .views import horoscopos_hoy, horoscopo_detail

urlpatterns = [
    path('horoscopos/', horoscopos_hoy, name='horoscopos_hoy'),
    path('horoscopos/<str:signo>/', horoscopo_detail, name='horoscopo_detail'),  #detail.html
    
]