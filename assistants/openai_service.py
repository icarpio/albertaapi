import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def create_assistant(name: str, instructions: str) -> dict:
    """
    Crea un asistente con OpenAI y devuelve dict serializable.
    """
    try:
        # Crear el asistente con la API beta
        assistant = openai.Client().beta.assistants.create(
            name=name,
            instructions=instructions,
            model="gpt-4o-mini"
        )

        # Retornar dict seguro
        return {
            "id": getattr(assistant, "id", None),
            "name": getattr(assistant, "name", name),
            "instructions": getattr(assistant, "instructions", instructions)
        }

    except Exception as e:
        raise Exception(f"Error al crear el asistente: {str(e)}")
