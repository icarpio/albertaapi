from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from .serializers import ContactSerializer
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def contact_api(request):
    print("📨 POST recibido")
    print("🧾 Content-Type recibido:", request.content_type)
    print("📦 Datos:", request.data)

    serializer = ContactSerializer(data=request.data)
    if not serializer.is_valid():
        print("❌ Errores del serializer:", serializer.errors)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        subject = data.get('subject', 'Sin asunto')
        from_email = os.getenv('EMAIL_USER', 'fallback@example.com')
        to_email = [from_email]
        reply_to = [data.get('email', '')]

        text_content = f"Mensaje de {data.get('first_name', '')} {data.get('last_name', '')} ({data.get('email', '')}):\n\n{data.get('message', '')}"
        
        html_content = f"""
        <div style="text-align: center;">
            <img src="cid:image1" alt="Imagen" style="display: inline-block; width: 32px; height: 32px;">
        </div>
        <p>Mensaje de <strong>{data.get('first_name', '')} {data.get('last_name', '')}</strong> ({data.get('email', '')}):</p>
        <p>{data.get('message', '').replace('\n', '<br>')}</p>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, reply_to=reply_to)
        msg.attach_alternative(html_content, "text/html")

        # ✅ Cargar imagen local al mismo nivel que views.py
        image_path = os.path.join(os.path.dirname(__file__), 'logo.png')
        print("📂 Cargando imagen desde:", image_path)

        with open(image_path, 'rb') as f:
            image_data = f.read()

        image = MIMEImage(image_data, _subtype='png')
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

        msg.send()
        print("✅ Correo enviado con imagen embebida")
        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error enviando el correo:", str(e))
        return Response({'success': False, 'errors': {'email': ['Error enviando email']}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

