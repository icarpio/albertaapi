from rest_framework import serializers
from .models import Horoscopo

class HoroscopoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horoscopo
        fields = ['signo', 'rango_fecha', 'fecha', 'texto']
