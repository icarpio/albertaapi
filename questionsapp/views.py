import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questions(request, num):
    if num < 1:
        return Response(
            {"error": "Número inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    questions = list(Question.objects.all())
    num = min(num, len(questions))
    selected = random.sample(questions, num)

    serializer = QuestionSerializer(selected, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def save_note(request):
    number = request.data.get("number")
    note = request.data.get("notes")

    try:
        question = Question.objects.get(number=number)
        question.notes = note
        question.save()
        return Response({"message": "Nota guardada"})
    except Question.DoesNotExist:
        return Response(
            {"error": "Pregunta no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )
