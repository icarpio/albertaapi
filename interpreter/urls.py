from django.urls import path
from . import views

urlpatterns = [
    path("transcribe/", views.transcribe_audio, name="transcribe"),
    path("translate/", views.translate_text, name="translate"),
    path("tts/", views.text_to_speech, name="tts"),
]