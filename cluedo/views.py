import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import GameState
import random
from .logic import get_npc_response, check_accusation, get_current_case,CASES, NPCS
import traceback  # 👈 Importante

@require_GET
def get_case(request):
    print(f"Method: {request.method}")
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
    try:
        data = json.loads(request.body)
        target = data.get("target")
        message = data.get("message")
        if not target or not message:
            return JsonResponse({"error": "Faltan parámetros"}, status=400)

        reply = get_npc_response(target, message)
        return JsonResponse({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()  # Imprime el error completo en consola
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@require_POST
def accuse(request):
    data = json.loads(request.body)
    npc_id = data.get("npc_id")
    if not npc_id:
        return JsonResponse({"error": "Falta npc_id"}, status=400)

    correct, message = check_accusation(npc_id)
    return JsonResponse({"correct": correct, "message": message})


@csrf_exempt
@require_POST
def restart_game_view(request):
    # Borra todo y crea nuevo estado
    GameState.objects.all().delete()
    
      # o de donde tengas tus datos

    new_case = random.choice(CASES)
    new_assassin = random.choice(list(NPCS.keys()))

    gs = GameState.objects.create(
        id=1,
        case_id=new_case["id"],
        assassin=new_assassin
    )

    return JsonResponse({
        "message": "Nuevo juego iniciado",
        "case": {
            "id": new_case["id"],
            "title": new_case["title"],
            "details": new_case["details"],
        }
        # "assassin": new_assassin  # ⚠️ para debug; no mostrar en frontend real
    })
