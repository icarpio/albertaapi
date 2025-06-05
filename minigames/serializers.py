from rest_framework import serializers
from .models import User, PlayerGameSession
from django.contrib.auth import authenticate

class MiniGameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'score', 'coins']

class PlayerGameSessionSerializer(serializers.ModelSerializer):
    played_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f%z') 
    class Meta:
        model = PlayerGameSession
        fields = ['game', 'score','played_at']  # No incluir 'user' aquí
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'score', 'coins']
        # <-- aquí marcamos score y coins como read-only
        read_only_fields = ['id', 'score', 'coins']

    def create(self, validated_data):
        # create_user ya maneja el hasheo de la contraseña
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        
        print(f"Intentando autenticar: {data['username']}")
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            print("Usuario autenticado")
        else:
            print("Autenticación fallida")
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas.")
