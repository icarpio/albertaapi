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

@api_view(['POST'])
@permission_classes([AllowAny])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        subject = data['subject']
        from_email = data['email']
        to_email = [os.getenv('EMAIL_USER')]

        text_content = f"Message from {data['first_name']} {data['last_name']} ({data['email']}):\n\n{data['message']}"
        html_content = f"""
        <div style="text-align: center;">
        <img src="cid:image1" alt="Image email" style="display: inline-block;">
        </div>
        <p>Message from <strong>{data['first_name']} {data['last_name']}</strong> ({data['email']}):</p>
        <p>{data['message'].replace('\n', '<br>')}</p>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")

        image_url = "https://upload.wikimedia.org/wikipedia/commons/b/b4/London_Eye_Twilight_April_2006.jpg"
        response = requests.get(image_url)
        image = MIMEImage(response.content)
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

        msg.send()

        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False, 'errors': serializer.errors}, status=400)
