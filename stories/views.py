
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Story
from .serializers import StorySerializer
import openai
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI")

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        prompt = (
            "Escribe un cuento corto, alegre, imaginativo y apropiado para niños. "
            "Incluye un protagonista simpático y una aventura divertida. "
            "Debe tener entre 150 y 300 palabras, ser positivo y fácil de entender."
        )
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=600,
                temperature=0.8,
            )
            return Response({"story": response.choices[0].text.strip()})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
