from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
import os
from .serializers import ContactSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection
from email.mime.image import MIMEImage
import requests
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
import os
import requests
from .serializers import ContactSerializer  # Asegúrate de que esto sea correcto

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser])  # Asegura que DRF parsee correctamente el JSON del frontend
def contact_api(request):
    # ✅ Debug útil para ver si el JSON llegó correctamente
    try:
        print("📥 request.body:", request.body.decode('utf-8'))
        print("📥 request.data (parsed):", request.data)
    except Exception as e:
        print("❌ Error leyendo el cuerpo:", e)
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # 🔧 Validamos con el serializer
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        subject = data['subject']
        from_email = data['email']
        to_email = [os.getenv('EMAIL_USER')]

        # Cuerpo del mensaje
        text_content = f"Message from {data['first_name']} {data['last_name']} ({data['email']}):\n\n{data['message']}"
        html_content = f"""
        <div style="text-align: center;">
            <img src="cid:image1" alt="Image email" style="display: inline-block;">
        </div>
        <p>Message from <strong>{data['first_name']} {data['last_name']}</strong> ({data['email']}):</p>
        <p>{data['message'].replace('\n', '<br>')}</p>
        """

        # Preparar y enviar correo
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        # Adjuntar imagen embebida
        try:
            image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b4/London_Eye_Twilight_April_2006.jpg"
            response = requests.get(image_url)
            image = MIMEImage(response.content)
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)
        except Exception as e:
            print("⚠️ No se pudo adjuntar la imagen:", e)

        msg.send()

        return JsonResponse({'success': True}, status=200)

    # ❌ Si hay errores de validación
    return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)

