import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .logic import get_npc_response, check_accusation, get_current_case

@require_GET
def get_case(request):
    case = get_current_case()
    if case:
        return JsonResponse({
            "title": case["title"],
            "description": case["description"],
            "details": case["details"],
        })
    return JsonResponse({"error": "No hay caso activo"}, status=404)

@csrf_exempt
@require_POST
def chat(request):
    data = json.loads(request.body)
    target = data.get("target")
    message = data.get("message")
    if not target or not message:
        return JsonResponse({"error": "Faltan parámetros"}, status=400)

    reply = get_npc_response(target, message)
    return JsonResponse({"reply": reply})

@csrf_exempt
@require_POST
def accuse(request):
    data = json.loads(request.body)
    npc_id = data.get("npc_id")
    if not npc_id:
        return JsonResponse({"error": "Falta npc_id"}, status=400)

    correct, message = check_accusation(npc_id)
    return JsonResponse({"correct": correct, "message": message})