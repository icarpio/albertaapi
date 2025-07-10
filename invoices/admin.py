from django.contrib import admin
from .models import Owner, Guest, Booking, Invoice

admin.site.register(Owner)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Invoice)