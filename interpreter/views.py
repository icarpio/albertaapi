import io
import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI"))

# POST /api/transcribe/
# Form-data: audio: <Blob webm/ogg/mp4/wav>
@csrf_exempt
def transcribe_audio(request):
    if request.method != "POST" or "audio" not in request.FILES:
        return JsonResponse({"error": "Send audio in multipart/form-data as 'audio'."}, status=400)
    audio = request.FILES["audio"]

    # El SDK acepta file-like objects
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=(audio.name, audio, audio.content_type),
        # language="auto"  # opcional; auto-detección
        # response_format="text"  # por defecto devuelve un objeto con .text
    )
    return JsonResponse({"text": transcript.text})

# POST /api/translate/
# JSON: { "text": "...", "target_lang": "es" }
@csrf_exempt
def translate_text(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    text = data.get("text", "").strip()
    target = data.get("target_lang", "es").strip()
    if not text:
        return JsonResponse({"error": "Field 'text' required"}, status=400)

    # Instrucción clara y breve para traducción
    prompt = (
        f"Traduce al {target}. Mantén el sentido, nombres propios y tono natural. "
        f"Solo la traducción, sin explicaciones.\n\nTexto:\n{text}"
    )
    # gpt-4o-mini
    resp = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt,
    )
    translated = resp.output_text  # texto llano agregado del output
    return JsonResponse({"translated_text": translated})

# POST /api/tts/
# JSON: { "text": "...", "voice": "alloy", "format": "mp3" }
@csrf_exempt
def text_to_speech(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "").strip()
        voice = data.get("voice", "alloy")
        fmt = data.get("format", "mp3")  # "mp3" | "wav" | "opus"

        if not text:
            return JsonResponse({"error": "Field 'text' required"}, status=400)

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            response_format=fmt,   # 👈 CORRECTO
        )

        audio_bytes = response.read()

        mime = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "opus": "audio/ogg"
        }.get(fmt, "audio/mpeg")

        return HttpResponse(audio_bytes, content_type=mime)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)