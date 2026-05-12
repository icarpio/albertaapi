from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import ContactSerializer
import os
import resend


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
        resend.api_key = os.environ.get("EMAIL_SEND")

        subject = data.get('subject', 'Sin asunto')

        text_content = (
            f"Mensaje de {data.get('first_name','')} {data.get('last_name','')} "
            f"({data.get('email','')}):\n\n"
            f"{data.get('message','')}"
        )

        # 🖼️ IMAGEN CORRECTA (IMPORTANTE: URL pública, NO archivo local)
        logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/500px-Coca-Cola_logo.svg.png"

        html_content = f"""
        <div style="font-family: Arial; text-align: center;">

            <img src="{logo_url}" width="80" style="margin-bottom:20px;" />

            <h2>📩 Nuevo mensaje de contacto</h2>

            <p>
                <strong>Nombre:</strong> {data.get('first_name','')} {data.get('last_name','')}<br>
                <strong>Email:</strong> {data.get('email','')}
            </p>

            <hr>

            <p style="text-align:left;">
                {data.get('message','').replace('\n','<br>')}
            </p>

        </div>
        """
        resend.Emails.send({
            "from": "Tu Web <onboarding@resend.dev>",
            "to": "icarpiodeveloper@gmail.com",
            "subject": subject,
            "text": text_content,
            "html": html_content,
            "reply_to": data.get('email', '')
        })

        print("✅ Email enviado correctamente con Resend")
        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        print("❌ Error enviando email:", str(e))
        return Response(
            {'success': False, 'errors': {'email': ['Error enviando email']}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )