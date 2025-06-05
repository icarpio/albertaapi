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

        if instance.game == "Comparación de sumas":
            if instance.score == 400:
                user.score += 400  # Ganó
            else:
                user.score = max(user.score - 400, 0)  # Perdió, no negativo
        else:
            user.score += instance.score

        user.save()

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
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Borra el token del usuario autenticado
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "Token no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
    
    
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)