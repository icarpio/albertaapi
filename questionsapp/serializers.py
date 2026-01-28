from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):

    def validate(self, data):
        options = data.get("options", {})
        correct = data.get("correct_answer")

        if not isinstance(options, dict) or len(options) < 2:
            raise serializers.ValidationError(
                "Debe haber al menos dos opciones."
            )

        valid_keys = set(options.keys())

        if isinstance(correct, str):
            correct = [correct]

        if not isinstance(correct, list):
            raise serializers.ValidationError(
                "correct_answer debe ser string o lista."
            )

        if not set(correct).issubset(valid_keys):
            raise serializers.ValidationError(
                "La respuesta correcta debe existir en options."
            )

        return data

    class Meta:
        model = Question
        fields = "__all__"
