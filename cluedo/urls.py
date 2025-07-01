from django.urls import path
from . import views

urlpatterns = [
    path("case/", views.get_case, name="get_case"),
    path("chat/", views.chat, name="chat"),
    path("accuse/", views.accuse, name="accuse"),
]
