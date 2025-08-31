# stories/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, HorrorStoryViewSet

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'horror', HorrorStoryViewSet, basename='horror')

urlpatterns = [
    path('', include(router.urls)),
]