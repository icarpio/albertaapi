from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Horoscopo
from .serializers import HoroscopoSerializer
from datetime import date
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def horoscopos_hoy(request):
    horoscopos = Horoscopo.objects.filter(fecha=date.today())
    serializer = HoroscopoSerializer(horoscopos, many=True)
    return Response(serializer.data)


compatibilidades = {
    "aries": ["leo", "sagitario", "geminis"],
    "tauro": ["virgo", "capricornio", "cancer"],
    "geminis": ["libra", "acuario", "aries"],
    "cancer": ["escorpio", "piscis", "tauro"],
    "leo": ["aries", "sagitario", "geminis"],
    "virgo": ["tauro", "capricornio", "cancer"],
    "libra": ["geminis", "acuario", "leo"],
    "escorpio": ["cancer", "piscis", "virgo"],
    "sagitario": ["aries", "leo", "acuario"],
    "capricornio": ["tauro", "virgo", "piscis"],
    "acuario": ["geminis", "libra", "sagitario"],
    "piscis": ["cancer", "escorpio", "capricornio"]
}
def signos_compatibles(signo):
    return compatibilidades.get(signo.lower(), [])

@api_view(['GET'])
@permission_classes([AllowAny])
def horoscopo_detail(request, signo):
    horoscopo = get_object_or_404(Horoscopo, signo__iexact=signo, fecha=date.today())
    serializer = HoroscopoSerializer(horoscopo)
    data = serializer.data
    data["compatibles"] = signos_compatibles(signo)  # <-- ahora sí incluimos compatibilidad
    return Response(data)