from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', MiniGameUserViewSet)
router.register(r'sessions', PlayerGameSessionViewSet,basename='sessions')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('shop/', shop_items_list),
    path('buy/', buy_item),
    path('inventory/', user_inventory),
]