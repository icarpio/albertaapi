from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os, requests
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
            <img src="cid:image1" alt="Imagen" style="display: inline-block;">
        </div>
        <p>Mensaje de <strong>{data.get('first_name', '')} {data.get('last_name', '')}</strong> ({data.get('email', '')}):</p>
        <p>{data.get('message', '').replace('\n', '<br>')}</p>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email, reply_to=reply_to)
        msg.attach_alternative(html_content, "text/html")

        # Descargar y adjuntar la imagen embebida
        image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b4/London_Eye_Twilight_April_2006.jpg"
        response = requests.get(image_url)

        if response.status_code == 200:
            image_data = response.content
            content_type = response.headers.get('Content-Type', '')
            subtype = 'jpeg'  # por defecto

            if content_type.startswith('image/'):
                subtype = content_type.split('/')[1]

            image = MIMEImage(image_data, _subtype=subtype)
            image.add_header('Content-ID', '<image1>')
            msg.attach(image)
        else:
            print("⚠️ No se pudo obtener la imagen:", image_url)

        msg.send()
        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error enviando el correo:", str(e))
        return Response({'success': False, 'errors': {'email': ['Error enviando email']}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

