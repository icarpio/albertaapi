import io
import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import traceback

# ❌ client global eliminado
# ✅ Creamos una función para inicializar el cliente cuando se necesite
def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# POST /api/transcribe/
# Form-data: audio: <Blob webm/ogg/mp4/wav>
@csrf_exempt
def transcribe_audio(request):
    if request.method != "POST" or "audio" not in request.FILES:
        return JsonResponse({"error": "Send audio in multipart/form-data as 'audio'."}, status=400)
    audio = request.FILES["audio"]

    client = get_openai_client()  # ✅ usar cliente aquí

    # El SDK acepta file-like objects
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=(audio.name, audio, audio.content_type),
    )
    return JsonResponse({"text": transcript.text})


# POST /api/translate/
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

    prompt = (
        f"Traduce al {target}. Mantén el sentido, nombres propios y tono natural. "
        f"Solo la traducción, sin explicaciones.\n\nTexto:\n{text}"
    )

    client = get_openai_client()  # ✅ usar cliente aquí
    resp = client.responses.create(
        model="gpt-3.5-turbo",
        input=prompt,
    )
    translated = resp.output_text
    return JsonResponse({"translated_text": translated})


# POST /api/tts/
@csrf_exempt
def text_to_speech(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "").strip()
        voice = data.get("voice", "alloy")
        fmt = data.get("format", "mp3")

        if not text:
            return JsonResponse({"error": "Field 'text' required"}, status=400)

        client = get_openai_client()  # ✅ usar cliente aquí
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            response_format=fmt,
        )

        audio_bytes = response.read()
        mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "opus": "audio/ogg"}.get(fmt, "audio/mpeg")

        return HttpResponse(audio_bytes, content_type=mime)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def text_to_speech_download(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
        text = data.get("text", "").strip()
        voice = data.get("voice", "alloy")

        if not text:
            return JsonResponse({"error": "Field 'text' required"}, status=400)

        client = get_openai_client()  # ✅ usar cliente aquí
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text,
            response_format="mp3"
        )

        audio_bytes = response.read()

        return HttpResponse(
            audio_bytes,
            content_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="tts.mp3"'}
        )

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
