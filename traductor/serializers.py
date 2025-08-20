from rest_framework import serializers
from .models import Traduccion

class TraduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traduccion
        fields = ['id', 'texto_original', 'español', 'ingles', 'italiano', 'fecha_creacion']