from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Traduccion
import openai
import os
from rest_framework.pagination import PageNumberPagination
from .models import Traduccion

openai.api_key = os.getenv("OPENAI")

IDIOMAS = {
    "español": "español",
    "ingles": "inglés británico",
    "italiano": "italiano"
}

@api_view(['POST'])
@permission_classes([AllowAny])
def traducir(request):
    texto = request.data.get("texto")
    if not texto:
        return Response({"error": "No hay texto para traducir"}, status=400)

    try:
        # Pedimos que traduzca a los tres idiomas en un solo mensaje
        prompt = (
            f"Traduce el siguiente texto a los tres idiomas y devuélvelo en formato JSON:\n\n"
            f"Texto: {texto}\n\n"
            "Formato JSON:\n"
            "{\n"
            "  \"español\": \"...\",\n"
            "  \"ingles\": \"...\",\n"
            "  \"italiano\": \"...\"\n"
            "}"
        )

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un traductor profesional."},
                {"role": "user", "content": prompt}
            ]
        )

        traducciones_raw = response.choices[0].message.content.strip()

        # Convertimos el string JSON a diccionario
        import json
        traducciones = json.loads(traducciones_raw)

        return Response({"traducciones": traducciones})

    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['POST'])
@permission_classes([AllowAny])
def saveTrans(request):
    data = request.data
    traducciones = data.get("traducciones")

    if not traducciones:
        return Response({"error": "No se enviaron traducciones"}, status=400)

    try:
        # Guardamos en el modelo
        nueva = Traduccion.objects.create(
            texto_original = data.get("texto_original", ""),
            español = traducciones.get("español", ""),
            ingles = traducciones.get("ingles", ""),
            italiano = traducciones.get("italiano", "")
        )
        nueva.save()
        return Response({"mensaje": "Traducciones guardadas correctamente"})

    except Exception as e:
        return Response({"error": str(e)}, status=500)



class TraduccionesPagination(PageNumberPagination):
    page_size = 10                        # ← 20 por página
    page_size_query_param = 'page_size'   # permite cambiarlo con ?page_size=xx
    max_page_size = 100                   # máximo permitido


@api_view(['GET'])
@permission_classes([AllowAny])
def listar_traducciones(request):
    try:
        traducciones = Traduccion.objects.all().order_by("-fecha_creacion")

        paginator = TraduccionesPagination()
        page = paginator.paginate_queryset(traducciones, request)

        lista = [
            {
                "id": t.id,
                "texto_original": t.texto_original,
                "español": t.español,
                "ingles": t.ingles,
                "italiano": t.italiano,
                "fecha_creacion": t.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if t.fecha_creacion else None
            }
            for t in page
        ]

        return paginator.get_paginated_response(lista)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete(request, id):
    try:
        traduccion = Traduccion.objects.get(pk=id)
        traduccion.delete()
        return Response({"mensaje": "Traducción eliminada correctamente"})
    except Traduccion.DoesNotExist:
        return Response({"error": "Traducción no encontrada"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
