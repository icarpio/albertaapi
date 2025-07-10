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

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        subject = data['subject']
        from_email = data['email']
        to_email = [os.getenv('EMAIL_USER')]

        # Mensaje plano
        text_content = f"Message from {data['first_name']} {data['last_name']} ({data['email']}):\n\n{data['message']}"

        # Mensaje HTML con imagen embebida
        html_content = f"""
        <div style="text-align: center;">
        <img src="cid:image1" alt="Image email" style="display: inline-block;">
        </div>
        <p>Message from <strong>{data['first_name']} {data['last_name']}</strong> ({data['email']}):</p>
        <p>{data['message'].replace('\n', '<br>')}</p>
        """

        # Crear mensaje
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        # Descargar la imagen y agregarla como MIMEImage
        image_url = "https://res.cloudinary.com/dsqk3zdtz/image/upload/v1737285162/profiles_sbfxzn.jpg"
        response = requests.get(image_url)
        image = MIMEImage(response.content)
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

        msg.send()

        return Response({'success': True}, status=status.HTTP_200_OK)

    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
