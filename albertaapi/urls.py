from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from invoices.views import CreateInvoiceView
from cvonline.views import contact_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/minigames/', include('minigames.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api2/stories/', include('stories.urls')),
    path('api3/cluedo/', include('cluedo.urls')),
    path('tarotapi/', include('tarotapi.urls')),
    path('api/create-invoice/', CreateInvoiceView.as_view(), name='create-invoice'),
    path('cv/contact/', contact_api, name='contact_api'),
]

handler404 = 'minigames.views.custom_404_view'  



