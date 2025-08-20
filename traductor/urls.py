from django.urls import path
from .views import traducir,saveTrans,listar_traducciones

urlpatterns = [
    path('traducir/', traducir, name='traducir'),
    path('save/', saveTrans),
    path('list/', listar_traducciones)
]