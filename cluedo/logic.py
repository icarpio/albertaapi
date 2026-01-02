import openai
import os
import random
from .models import GameState

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


CASES = [
    {
        "id": 1,
        "title": "Asesinato en la mansión",
        "description": "Esta noche hubo un asesinato en la mansión. El cuerpo fue encontrado en la biblioteca con signos de lucha.",
        "details": (
            "El mayordomo estaba ausente a las 11pm. "
            "La jardinera vio una sombra sospechosa cerca de la biblioteca. "
            "El vecino curioso merodeaba por los pasillos intentando escuchar conversaciones. "
            "El detective retirado había sido invitado por la víctima para una consulta privada. "
            "El periodista llegó inesperadamente, buscando una exclusiva. "
            "El chef discutió con la víctima por un cambio de menú de última hora. "
            "La anciana afirmó haber visto a alguien salir corriendo, pero no recuerda quién. "
            "El niño prodigio encontró una pluma ensangrentada bajo una alfombra."
        )
    },
    {
        "id": 2,
        "title": "El misterio del robo",
        "description": "Un valioso diamante desapareció durante la fiesta en la villa.",
        "details": (
            "El chef estaba en la cocina pero parecía nervioso. "
            "El vecino tenía una coartada dudosa. "
            "El mayordomo fue quien recibió al joyero esa noche. "
            "La jardinera encontró tierra suelta cerca de la caja fuerte. "
            "El detective retirado señaló que alguien había manipulado las cámaras. "
            "La anciana confundió la caja del diamante con una caja de bombones. "
            "El periodista fue sorprendido husmeando en el despacho. "
            "El niño prodigio descubrió una huella pequeña en el cristal del expositor."
        )
    },
    {
        "id": 3,
        "title": "El secreto del sótano",
        "description": "Se encontraron huellas extrañas en el sótano de la casa.",
        "details": (
            "La anciana escuchó ruidos extraños a medianoche. "
            "El periodista investigaba un caso antiguo relacionado con la familia. "
            "El chef bajó a buscar un vino raro, pero tardó más de lo normal. "
            "El mayordomo guardaba documentos en una caja oculta. "
            "La jardinera dejó herramientas olvidadas allí días antes. "
            "El vecino vio luces encenderse cuando todos dormían. "
            "El detective retirado sospechó que se usó una entrada secreta. "
            "El niño prodigio halló símbolos escritos con tiza en la pared."
        )
    },
    {
        "id": 4,
        "title": "La desaparición del testigo",
        "description": "Un testigo clave desapareció justo antes del juicio.",
        "details": (
            "El niño prodigio vio una figura sospechosa saliendo por la puerta trasera. "
            "El detective retirado estaba vigilando la zona por encargo. "
            "El periodista había contactado al testigo para una entrevista. "
            "La jardinera escuchó un grito ahogado cerca del invernadero. "
            "El mayordomo dijo haber preparado la habitación del testigo. "
            "El chef notó que faltaba comida del refrigerador. "
            "La anciana dijo que alguien entró en su habitación confundido. "
            "El vecino se ofreció a ayudar con la búsqueda, pero desapareció por horas."
        )
    },
    {
        "id": 5,
        "title": "El veneno en la cena",
        "description": "Alguien fue envenenado durante la cena de gala.",
        "details": (
            "El chef preparó el plato principal con ingredientes inusuales. "
            "La jardinera manipuló las flores que decoraban la mesa. "
            "El mayordomo sirvió el vino, pero no bebió nada. "
            "El periodista estaba investigando a uno de los invitados. "
            "La anciana notó un sabor extraño en su sopa, pero no dijo nada. "
            "El detective retirado revisó la cocina tras el incidente. "
            "El niño prodigio detectó un patrón en los platos afectados. "
            "El vecino fue visto con una caja misteriosa cerca de la despensa."
        )
    },
    {
        "id": 6,
        "title": "La carta anónima",
        "description": "Una carta anónima amenazante fue recibida por la víctima.",
        "details": (
            "El mayordomo encontró la carta en el despacho. "
            "El vecino actuó de manera nerviosa tras la llegada del sobre. "
            "El periodista reconoció el tipo de letra usada. "
            "La jardinera dijo haber visto a alguien merodear por el buzón. "
            "El chef negó saber escribir a máquina, pero tenía tinta en las manos. "
            "La anciana creyó que era una carta de amor mal escrita. "
            "El detective retirado detectó que la carta usaba papel del archivo familiar. "
            "El niño prodigio descubrió que el sobre había sido manipulado con guantes."
        )
    },
    {
        "id": 7,
        "title": "El robo del cuadro",
        "description": "Un cuadro valioso desapareció sin dejar rastro.",
        "details": (
            "La anciana cuidaba la galería, pero se quedó dormida. "
            "El periodista había estado investigando al dueño del cuadro. "
            "El mayordomo tenía la llave del salón donde colgaba la obra. "
            "La jardinera limpiaba una planta cercana y escuchó un ruido sordo. "
            "El chef fue visto en la galería, buscando especias para una receta. "
            "El vecino aseguró haber visto una figura encapuchada. "
            "El detective retirado notó que la alarma fue desactivada manualmente. "
            "El niño prodigio encontró restos de pintura en el suelo."
        )
    },
    {
        "id": 8,
        "title": "El encuentro en la biblioteca",
        "description": "Dos personas discutieron acaloradamente en la biblioteca horas antes del crimen.",
        "details": (
            "El detective retirado escuchó la discusión desde el pasillo. "
            "El niño prodigio encontró una nota misteriosa con amenazas. "
            "El mayordomo fue quien abrió la biblioteca esa noche. "
            "La jardinera limpiaba las ventanas y vio a los dos sujetos discutir. "
            "El periodista intentó grabar la conversación, pero fue descubierto. "
            "La anciana confundió la discusión con una obra de teatro. "
            "El chef dijo haber oído el ruido mientras preparaba una infusión. "
            "El vecino fue visto saliendo apresuradamente tras la pelea."
        )
    },
    {
        "id": 9,
        "title": "El teléfono desconectado",
        "description": "El teléfono de la víctima fue desconectado justo antes del ataque.",
        "details": (
            "El mayordomo fue el último en usar el teléfono. "
            "La jardinera estaba cerca de la centralita revisando un enchufe. "
            "El periodista intentaba llamar a su editor, pero la línea no funcionaba. "
            "El chef culpó al cableado viejo, aunque sabía repararlo. "
            "El detective retirado revisó el cableado tras el incidente. "
            "La anciana intentó llamar a su nieta y no obtuvo tono. "
            "El niño prodigio encontró marcas de corte en el cable. "
            "El vecino dijo que escuchó interferencias antes del corte."
        )
    },
    {
        "id": 10,
        "title": "El testamento perdido",
        "description": "El testamento de la víctima desapareció misteriosamente.",
        "details": (
            "El vecino estuvo revisando documentos antiguos. "
            "El chef escuchó conversaciones sobre una posible herencia. "
            "El mayordomo tenía acceso a la caja fuerte donde estaba guardado. "
            "La jardinera encontró papeles quemados cerca del invernadero. "
            "El periodista sabía del testamento y preparaba un artículo. "
            "La anciana dijo que lo vio por última vez en el escritorio. "
            "El detective retirado halló un compartimento oculto vacío. "
            "El niño prodigio notó que faltaba una página del registro familiar."
        )
    }
]


NPCS = {
    "npc1": "Eres un mayordomo educado pero reservado.",
    "npc2": "Eres una jardinera que oculta cosas.",
    "npc3": "Eres un vecino curioso.",
    "npc4": "Eres un detective retirado, sabio pero escéptico.",
    "npc5": "Eres una periodista ambiciosa.",
    "npc6": "Eres un chef excéntrico y observador.",
    "npc7": "Eres una anciana sabia, algo olvidadiza.",
    "npc8": "Eres un niño prodigio muy observador."
}

# ---------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------

def reset_gamestate():
    """Crea un nuevo juego con un caso y asesino aleatorio."""
    GameState.objects.filter(id=1).delete()
    gs = GameState.objects.create(
        id=1,
        assassin=random.choice(list(NPCS.keys())),
        case_id=random.choice(CASES)["id"]
    )
    return gs


def get_gamestate():
    """Devuelve el estado actual sin modificarlo.
       Si no existe, crea uno nuevo."""
    try:
        return GameState.objects.get(id=1)
    except GameState.DoesNotExist:
        return reset_gamestate()


def get_current_case():
    gs = get_gamestate()
    for case in CASES:
        if case["id"] == gs.case_id:
            return case
    return None


# ---------------------------------------------
# PROMPT CREATION
# ---------------------------------------------

def get_npc_prompt(npc_id):
    gs = get_gamestate()
    assassin = gs.assassin
    case = get_current_case()

    # Contexto del caso
    case_context = (
        f"Caso: {case['title']}\n"
        f"Descripción: {case['description']}\n"
        f"Detalles conocidos: {case['details']}\n\n"
        "IMPORTANTE: Puedes ampliar, inferir o añadir detalles menores "
        "siempre que no contradigas los hechos principales.\n\n"
    )

    # Rol base del NPC
    npc_personality = NPCS[npc_id]

    # Inocentes vs Asesino
    if npc_id == assassin:
        role = (
            "Eres el asesino. Debes mentir con creatividad, ofrecer coartadas nuevas, "
            "desviar sospechas y generar detalles falsos que parezcan plausibles. "
            "Tu objetivo es confundir."
        )
    else:
        role = (
            "Eres inocente. Ayudas con sinceridad e intentas aportar "
            "recuerdos, impresiones, pistas nuevas o teorías razonables "
            "que no están explícitamente en los detalles pero que podrían ayudar al jugador."
        )

    # Forma de hablar
    style = (
        "Responde siempre en primera persona, como si realmente estuvieras allí. "
        "NO pongas tu nombre ni etiquetas. No repitas literalmente las frases del caso. "
        "Cada respuesta debe aportar algo nuevo: una observación, un detalle, "
        "una emoción, una suposición o un recuerdo."
    )

    return f"{case_context}{npc_personality} {role} {style}"


# ---------------------------------------------
# NPC RESPONSE GENERATION
# ---------------------------------------------

def get_npc_response(npc_id, history):
    """
    history debe ser una lista de mensajes:
    [
        {"role": "user", "content": "texto del jugador"},
        {"role": "assistant", "content": "respuesta anterior del NPC"},
        ...
    ]
    """
    if not isinstance(history, list):
        # Fallback en caso de que aún lo envíes como texto
        history = [{"role": "user", "content": history}]

    system_prompt = get_npc_prompt(npc_id)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",             
        messages=messages,
        temperature=0.80,                
        max_tokens=250,
        presence_penalty=0.8,             
        frequency_penalty=0.4
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------
# ACCUSATION CHECK
# ---------------------------------------------

def check_accusation(npc_id):
    gs = get_gamestate()
    if npc_id == gs.assassin:
        return True, f"¡Correcto! {npc_id} es el culpable. Has resuelto el caso."
    else:
        return False, f"No, {npc_id} no es el culpable. Sigue investigando."
