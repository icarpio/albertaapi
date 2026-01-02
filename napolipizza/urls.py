from django.urls import path
from .views import order_api, menu_api

urlpatterns = [
    path('order/', order_api, name='order_api'),
    path('menu/', menu_api, name='menu_api'),
]