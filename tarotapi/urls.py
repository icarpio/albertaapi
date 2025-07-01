from django.urls import path
from .views import draw_tarot

urlpatterns = [
    path("draw/", draw_tarot),
]