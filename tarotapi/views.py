import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .cards import draw_cards
from .prompts import build_prompt
import openai

client = openai.OpenAI(api_key=settings.OPENAI)

@csrf_exempt
def draw_tarot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        spread = data.get("spread", 3)
        cards = draw_cards(spread)
        prompt = build_prompt(cards, spread)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # modelo más económico y rápido
            messages=[
                {"role": "system", "content": "Eres una tarotista sabia y espiritual."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )

        interpretation = response.choices[0].message.content

        return JsonResponse({"cards": cards, "interpretation": interpretation})

    return JsonResponse({"error": "Método no permitido"}, status=405)



#Temperatura baja (0.2–0.5): hace respuestas más directas y menos creativas.
#Temperatura alta (>0.7): respuestas más elaboradas y creativas, puede alargar el texto.