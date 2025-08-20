from django.urls import path
from .views import traducir,saveTrans,listar_traducciones,delete

urlpatterns = [
    path('traducir/', traducir, name='traducir'),
    path('save/', saveTrans),
    path('list/', listar_traducciones),
    path("delete/<int:id>/", delete, name="borrar_traduccion"),
]