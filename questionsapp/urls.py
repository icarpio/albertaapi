from django.urls import path
from .views import get_questions, save_note

urlpatterns = [
    path("questions/<int:num>/", get_questions),
    path("save-note/", save_note),
]
