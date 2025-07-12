
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
import requests

from .serializers import ContactSerializer  # Asegúrate de importar tu serializer correctamente

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_api(request):
    print("🔥 Entrando a contact_api PRODUCCIÓN")
    print("📦 Datos recibidos:", request.data)
    print("🧾 Content-Type:", request.content_type)

    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        print("✅ Datos validados:", data)

        subject = data['subject']
        from_email = data['email']
        to_email = [os.getenv('EMAIL_USER') or 'tu@email.com']  # fallback si no está la variable

        text_content = f"Message from {data['first_name']} {data['last_name']} ({data['email']}):\n\n{data['message']}"
        html_content = f"""
        <div style="text-align: center;">
            <img src="cid:image1" alt="Image email" style="display: inline-block;">
        </div>
        <p>Message from <strong>{data['first_name']} {data['last_name']}</strong> ({data['email']}):</p>
        <p>{data['message'].replace('\n', '<br>')}</p>
        """

        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")

            # Adjuntar imagen externa
            image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b4/London_Eye_Twilight_April_2006.jpg"
            response = requests.get(image_url)
            image = MIMEImage(response.content)
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)

            msg.send()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print("❌ Error enviando correo:", str(e))
            return Response({'success': False, 'errors': {'email': ['Error enviando email']}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        print("❌ Errores de validación:", serializer.errors)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
