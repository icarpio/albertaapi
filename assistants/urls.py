from django.urls import path
from . import views

urlpatterns = [
    path("create-assistant/", views.create_assistant_view),
    path("get-response/", views.get_response),
    path("reset-thread/", views.reset_thread, name="reset_thread"),
]
