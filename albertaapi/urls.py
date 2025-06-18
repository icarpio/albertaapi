from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/minigames/', include('minigames.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api2/stories/', include('stories.urls')),
    path('api3/cluedo/', include('cluedo.urls')),
]

handler404 = 'minigames.views.custom_404_view'