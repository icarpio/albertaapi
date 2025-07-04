from rest_framework.routers import DefaultRouter
from .views import StoryViewSet

router = DefaultRouter()
router.register(r'stories', StoryViewSet, basename='story')
urlpatterns = router.urls