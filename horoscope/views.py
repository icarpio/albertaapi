from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Horoscopo
from .serializers import HoroscopoSerializer
from datetime import date

@api_view(['GET'])
@permission_classes([AllowAny])
def horoscopos_hoy(request):
    horoscopos = Horoscopo.objects.filter(fecha=date.today())
    serializer = HoroscopoSerializer(horoscopos, many=True)
    return Response(serializer.data)


