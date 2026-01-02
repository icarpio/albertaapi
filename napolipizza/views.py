from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from .serializers import OrderSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Pizza
from .serializers import PizzaSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def order_api(request):
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Guardar el pedido
    order = serializer.save()

    try:
        from_email = os.getenv('EMAIL_USER', 'fallback@example.com')
        total = order.total_price()

        # --- Enviar email al restaurante ---
        subject_restaurant = f"Nuevo pedido de {order.customer_name}"
        to_email_restaurant = [from_email]

        items_text_list = []
        items_html_list = []
        for item in order.items.all():
            subtotal = item.quantity * item.pizza.price
            items_text_list.append(f"{item.quantity} x {item.pizza.name} - ${item.pizza.price} c/u - Subtotal: ${subtotal}")
            items_html_list.append(f"<p>{item.quantity} x {item.pizza.name} - ${item.pizza.price} c/u - Subtotal: ${subtotal}</p>")

        items_text = "\n".join(items_text_list)
        items_html = "".join(items_html_list)

        text_content_restaurant = f"""
Nuevo pedido recibido:

Cliente: {order.customer_name}
Email: {order.customer_email}
Teléfono: {order.customer_phone}
Pizzas:
{items_text}

Mensaje adicional: {order.message or ''}
Total: ${total}
"""

        html_content_restaurant = f"""
<h2>Nuevo Pedido de Pizza</h2>
<p><img src="cid:image1" alt="Pizza"/></p>
<p><strong>Cliente:</strong> {order.customer_name}</p>
<p><strong>Email:</strong> {order.customer_email}</p>
<p><strong>Teléfono:</strong> {order.customer_phone}</p>
<h3>Pizzas:</h3>
{items_html}
<p><strong>Mensaje adicional:</strong> {order.message or ''}</p>
<p><strong>Total:</strong> ${total}</p>
"""

        msg_restaurant = EmailMultiAlternatives(subject_restaurant, text_content_restaurant, from_email, to_email_restaurant)
        msg_restaurant.attach_alternative(html_content_restaurant, "text/html")

        # Imagen embebida
        image_path = os.path.join(os.path.dirname(__file__), 'pizza.png')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data, _subtype='png')
            image.add_header('Content-ID', '<image1>')
            msg_restaurant.attach(image)

        msg_restaurant.send()

        # --- Enviar correo de confirmación al cliente ---
        subject_client = f"Confirmación de tu pedido, {order.customer_name}"
        to_email_client = [order.customer_email]

        text_content_client = f"""
        Hola {order.customer_name},

        Hemos recibido tu pedido de pizza correctamente. Aquí están los detalles:

        Pizzas:
        {items_text}

        Total: ${total}

        ¡Gracias por tu preferencia!
        """

        html_content_client = f"""
        <h1 style="display: flex; align-items: center; gap: 10px;">
        Napoli Pizza
        <img src="cid:image1" alt="Pizza" style="height: 50px;"/>
        </h1>
        <h2>Tu pedido ha sido recibido</h2>
        <p>Hola <strong>{order.customer_name}</strong>,</p>
        <p>Hemos recibido tu pedido de pizza correctamente. Aquí están los detalles:</p>
        {items_html}
        <p><strong>Total:</strong> ${total}</p>
        <p>¡Gracias por tu preferencia!</p>
        """

        msg_client = EmailMultiAlternatives(subject_client, text_content_client, from_email, to_email_client)
        msg_client.attach_alternative(html_content_client, "text/html")

        # Imagen embebida para el cliente
        image_path = os.path.join(os.path.dirname(__file__), 'pizza.png')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
            image = MIMEImage(img_data, _subtype='png')
            image.add_header('Content-ID', '<image1>')
            msg_client.attach(image)  # <-- aquí se adjunta al mensaje correcto

        msg_client.send()


        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'errors': {'email': ['Error enviando email', str(e)]}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_api(request):
    try:
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)