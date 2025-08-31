# stories/views.py
import os
from dotenv import load_dotenv
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import openai
import random
from .models import Story, HorrorStory
from .serializers import StorySerializer, HorrorStorySerializer

load_dotenv()

# Nueva forma en openai>=1.0.0
client = openai.OpenAI(api_key=os.getenv("OPENAI"))

class StoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
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
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un escritor de cuentos para niños."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.8,
            )
            story_text = response.choices[0].message.content.strip()
            return Response({"story": story_text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class HorrorStoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = HorrorStory.objects.all().order_by('-created_at')
    serializer_class = HorrorStorySerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        openings = [
            "Una noche oscura y silenciosa,",
            "Bajo la lluvia intensa,",
            "Un extraño sonido resonó mientras",
            "En lo profundo del bosque,",
            "En el borde del pueblo desierto,"
        ]

        protagonists = [
            "un niño valiente pero asustado",
            "una joven curiosa con un secreto oscuro",
            "un anciano solitario atormentado por el pasado",
            "una mujer atrapada en sus peores pesadillas",
            "un detective obsesionado con lo paranormal"
        ]

        settings = [
            "en un bosque oscuro y siniestro donde susurran las sombras",
            "en una mansión abandonada llena de ecos y susurros",
            "en un pueblo desierto donde nadie quiere volver",
            "en una cabaña aislada rodeada por la niebla eterna",
            "en un hospital psiquiátrico olvidado por el tiempo"
        ]

        situations = [
            "escucha pasos misteriosos que se acercan lentamente",
            "ve sombras que se retuercen con formas humanas",
            "siente una presencia helada que lo sigue a todas partes",
            "encuentra un objeto maldito que le roba la cordura",
            "una puerta se abre sola revelando un vacío infinito",
            "recibe mensajes crípticos escritos con sangre fresca"
        ]

        prompt = (
            f"{random.choice(openings)} {random.choice(protagonists)} enfrentando situaciones misteriosas "
            f"{random.choice(settings)}. Durante la historia, {random.choice(situations)}. "
            f"Debe tener entre 150 y 300 palabras, crear tensión y ser envolvente, sin lenguaje ofensivo."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un escritor creativo de historias de terror. Evita repetir frases iniciales comunes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.9,
                top_p=0.9
            )
            story_text = response.choices[0].message.content.strip()
            return Response({"story": story_text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
