from rest_framework import viewsets, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, PlayerGameSession
from .serializers import MiniGameUserSerializer, PlayerGameSessionSerializer, RegisterSerializer, LoginSerializer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ShopItem, Purchase
import logging

logger = logging.getLogger(__name__)

class MiniGameUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MiniGameUserSerializer


class PlayerGameSessionViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerGameSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo sesiones del usuario autenticado
        return PlayerGameSession.objects.filter(user=self.request.user).order_by('-played_at')

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(user=user)

        if instance.game == "Comparacion de sumas":
            # Reglas para Comparacion de sumas
            if instance.score == 400:
                user.score += 400  # Ganó
            #elif instance.score == 200:
                #user.score += 100  # Buen intento
            else:
                user.score = max(user.score - 400, 0)  # Perdió, no negativo

        elif instance.game == "OTRO JUEGO":
            # Reglas para OTRO JUEGO
            if instance.score == 300:
                user.score += 300  # Ganó muy bien
            elif instance.score == 150:
                user.score += 75   # Ganó parcialmente
            else:
                user.score = max(user.score - 200, 0)  # Perdió, no negativo

        elif instance.game == "PPT":
            # Reglas para Piedra Papel Tijera
            if instance.score > 0:
                user.score += instance.score  # Ganó suma puntos
            else:
                user.score = max(user.score + instance.score - 400, 0)  # Penalización, no negativo

        else:
            # Otros juegos, sumar directo
            user.score += instance.score

        user.save()


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permite acceso sin autenticación

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = serializer.save()
            # Aquí puedes generar token si quieres, o devolver solo usuario
            return Response({
                "id": user.id,
                "username": user.username,
                "score": user.score,
                "coins": user.coins,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": "Error interno al crear usuario."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
@method_decorator(csrf_exempt, name='dispatch')      
class LoginView(APIView):
    permission_classes = [AllowAny]  # Para evitar 401

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "score": user.score,
            "coins": user.coins,
        })

@method_decorator(csrf_exempt, name='dispatch')        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Borra el token del usuario autenticado
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Token no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_score_to_coins(request):
    try:
        user = request.user
        points_to_convert = int(request.data.get('points', 0))

        if points_to_convert <= 0 or points_to_convert > user.score:
            return Response({'error': 'No tienes puntos suficientes'}, status=400)

        if points_to_convert < 100:
            return Response({'error': 'Debes convertir al menos 100 puntos.'}, status=400)

        coins_earned = points_to_convert // 100
        points_spent = coins_earned * 100

        # Asegúrate de que score y coins no sean None
        if user.score is None:
            user.score = 0
        if user.coins is None:
            user.coins = 0

        user.score -= points_spent
        user.coins += coins_earned
        user.save()

        return Response({
            'coins_earned': coins_earned,
            'points_spent': points_spent,
            'remaining_score': user.score,
            'new_balance': user.coins
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': 'Internal Server Error', 'details': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shop_items_list(request):
    try:
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)

        items = ShopItem.objects.all().values('id', 'name', 'price', 'image_name')
        return Response(list(items))
    except Exception as e:
        print("Error en shop_items_list:", str(e))
        return Response({'error': 'Error interno del servidor'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_item(request):
    user = request.user
    item_id = request.data.get('item_id')

    try:
        item = ShopItem.objects.get(pk=item_id)
    except ShopItem.DoesNotExist:
        return Response({'error': 'Ítem no encontrado'}, status=404)

    if user.coins < item.price:
        return Response({'error': 'No tienes suficientes monedas'}, status=400)

    user.coins -= item.price
    user.save()
    Purchase.objects.create(user=user, item=item)

    return Response({
        'message': 'Ítem comprado',
        'item': item.name,
        'coins_left': user.coins
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_inventory(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('item')
    data = [
        {
            'item_id': p.item.id,
            'name': p.item.name,
            'image_name': p.item.image_name,
            'purchased_at': p.purchased_at
        } for p in purchases
    ]
    return Response(data)

    
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)



"""
def perform_create(self, serializer):
    user = self.request.user
    instance = serializer.save(user=user)

    if instance.game == "Comparacion de sumas":
        # lógica para Comparacion de sumas
        pass
    elif instance.game in ("PPT", "SUMA"):
        # lógica para PPT o SUMA juntos
        pass
    else:
        user.score += instance.score

    user.save()
"""