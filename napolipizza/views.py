from .serializers import OrderSerializer
from .models import Pizza
from .serializers import PizzaSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import OrderSerializer
import os
import resend


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def order_api(request):

    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'success': False, 'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    order = serializer.save()

    try:
        resend.api_key = os.environ.get("EMAIL_SEND")

        from_email = "Napoli Pizza <onboarding@resend.dev>"
        total = order.total_price()

        # 🧾 ITEMS
        items_text_list = []
        items_html_list = []

        for item in order.items.all():
            subtotal = item.quantity * item.pizza.price
            items_text_list.append(
                f"{item.quantity} x {item.pizza.name} - ${item.pizza.price} c/u - Subtotal: ${subtotal}"
            )
            items_html_list.append(
                f"<p>{item.quantity} x {item.pizza.name} - ${item.pizza.price} c/u - Subtotal: ${subtotal}</p>"
            )

        items_text = "\n".join(items_text_list)
        items_html = "".join(items_html_list)

        # 🖼️ IMAGEN (URL pública, NO archivo local)
        pizza_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/500px-Coca-Cola_logo.svg.png"

        # =========================
        # 📩 EMAIL RESTAURANTE
        # =========================

        subject_restaurant = f"Nuevo pedido de {order.customer_name}"

        text_restaurant = f"""
Nuevo pedido recibido:

Cliente: {order.customer_name}
Email: {order.customer_email}
Teléfono: {order.customer_phone}

Pizzas:
{items_text}

Mensaje: {order.message or ''}

Total: ${total}
"""

        html_restaurant = f"""
        <div style="font-family: Arial;">
            <h2>🍕 Nuevo Pedido de Pizza</h2>
            <img src="{pizza_img}" width="120" />
            <p><strong>Cliente:</strong> {order.customer_name}</p>
            <p><strong>Email:</strong> {order.customer_email}</p>
            <p><strong>Teléfono:</strong> {order.customer_phone}</p>
            <h3>Pizzas:</h3>
            {items_html}
            <p><strong>Mensaje:</strong> {order.message or ''}</p>
            <h3>Total: ${total}</h3>
        </div>
        """
        resend.Emails.send({
            "from": from_email,
            "to": ["icarpiodeveloper@gmail.com"],
            "subject": subject_restaurant,
            "text": text_restaurant,
            "html": html_restaurant,
            "reply_to": order.customer_email
        })

        # =========================
        # 📩 EMAIL CLIENTE
        # =========================

        subject_client = f"Confirmación de tu pedido, {order.customer_name}"

        text_client = f"""
Hola {order.customer_name},

Hemos recibido tu pedido correctamente.

Pizzas:
{items_text}

Total: ${total}

¡Gracias por tu compra!
"""

        html_client = f"""
        <div style="font-family: Arial; text-align: center;">
            <h1>
                Napoli Pizza
            </h1>

            <img src="{pizza_img}" width="100" />

            <h2>Tu pedido ha sido recibido 🍕</h2>
            <p>Hola <strong>{order.customer_name}</strong></p>

            {items_html}

            <h3>Total: ${total}</h3>

            <p>¡Gracias por tu preferencia!</p>
        </div>
        """

        resend.Emails.send({
            "from": from_email,
            "to": [order.customer_email],
            "subject": subject_client,
            "text": text_client,
            "html": html_client,
        })

        return Response({'success': True}, status=status.HTTP_200_OK)

    except Exception as e:
        print("ERROR EMAIL:", e)
        return Response(
            {'success': False, 'errors': {'email': ['Error enviando email']}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def menu_api(request):
    try:
        pizzas = Pizza.objects.all()
        serializer = PizzaSerializer(pizzas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)