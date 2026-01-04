import time
import traceback
import openai

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .openai_service import create_assistant
from django_ratelimit.decorators import ratelimit


# ===============================
# Cliente OpenAI
# ===============================
client = openai.Client(api_key=settings.OPENAI_API_KEY)


# ===============================
# API: Crear asistente
# ===============================
@csrf_exempt
@require_POST
def create_assistant_view(request):
    try:
        name = request.POST.get("name", "").strip()
        instructions = request.POST.get("instructions", "").strip()

        if not name or not instructions:
            return JsonResponse(
                {"error": "Faltan datos"},
                status=400
            )

        assistant = create_assistant(name, instructions)

        assistant_id = assistant.get("id")
        assistant_name = assistant.get("name")

        if not assistant_id:
            return JsonResponse(
                {"error": "No se pudo crear el asistente"},
                status=500
            )

        # Guardar estado en sesión
        request.session["assistant_id"] = assistant_id
        request.session["assistant_name"] = assistant_name
        request.session.pop("thread_id", None)

        return JsonResponse({
            "assistant_id": assistant_id,
            "name": assistant_name,
            "instructions": assistant.get("instructions"),
            "message": "Asistente creado correctamente"
        })

    except Exception as e:
        return JsonResponse({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500)


# ===============================
# API: Chat con asistente
# ===============================


@csrf_exempt
@require_POST
@ratelimit(key="ip", rate="5/m", block=True)
def get_response(request):
    """
    Recibe el mensaje del usuario y mantiene continuidad usando el mismo thread.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        user_message = request.POST.get("message", "").strip()
        assistant_id = request.POST.get("assistant_id")

        if not user_message:
            return JsonResponse({"error": "Mensaje vacío"}, status=400)
        if not assistant_id:
            return JsonResponse({"error": "No hay asistente activo"}, status=400)

        # Reutilizar el mismo thread usando sesión
        thread_id = request.session.get("thread_id")
        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id
            request.session["thread_id"] = thread_id

        # Añadir mensaje del usuario
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Ejecutar asistente
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Esperar a que termine
        for _ in range(30):
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            if run_status.status in ["failed", "cancelled", "expired"]:
                return JsonResponse({"error": "Falló la ejecución del asistente"}, status=500)
            time.sleep(1)
        else:
            return JsonResponse({"error": "Tiempo de espera agotado"}, status=500)

        # Obtener último mensaje del asistente
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            limit=1
        )

        if messages.data and messages.data[0].role == "assistant":
            return JsonResponse({
                "message": messages.data[0].content[0].text.value
            })

        return JsonResponse({"error": "No se recibió respuesta"}, status=500)

    except Exception as e:
        import traceback
        return JsonResponse({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500)


@csrf_exempt
@require_POST
def reset_thread(request):
    """
    Reinicia el chat eliminando el thread_id de la sesión.
    """
    try:
        request.session.pop("thread_id", None)
        return JsonResponse({"message": "Chat reiniciado correctamente"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)