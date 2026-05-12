from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
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
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    try:
        subject = data.get('subject', 'Sin asunto')

        from_email = os.getenv('EMAIL_USER', 'fallback@example.com')
        to_email = [from_email]
        reply_to = [data.get('email', '')]

        # 📄 Texto plano
        text_content = (
            f"Mensaje de {data.get('first_name', '')} {data.get('last_name', '')} "
            f"({data.get('email', '')}):\n\n"
            f"{data.get('message', '')}"
        )

        # 🌐 HTML SIN imagen
        html_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h2>Nuevo mensaje de contacto</h2>
            <p>
                <strong>Nombre:</strong> {data.get('first_name', '')} {data.get('last_name', '')}<br>
                <strong>Email:</strong> {data.get('email', '')}
            </p>
            <hr>
            <p>{data.get('message', '').replace('\n', '<br>')}</p>
        </div>
        """

        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to_email,
            reply_to=reply_to
        )

        msg.attach_alternative(html_content, "text/html")

        msg.send()

        print("✅ Correo enviado correctamente")
        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error enviando el correo:", str(e))
        return Response(
            {'success': False, 'errors': {'email': ['Error enviando email']}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )