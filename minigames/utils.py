from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Primero usa el manejador por defecto
    response = exception_handler(exc, context)

    if response is None:
        # Aquí podemos manejar excepciones no manejadas, incluido 404
        return Response({
            "detail": "La ruta que buscas no existe."
        }, status=status.HTTP_404_NOT_FOUND)

    if response.status_code == 404:
        # Modificamos el mensaje para 404 si queremos
        response.data = {"detail": "Recurso no encontrado (404)"}

    return response
