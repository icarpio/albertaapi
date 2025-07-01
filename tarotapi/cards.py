import random

TAROT_CARDS = [
    "El Loco", "El Mago", "La Sacerdotisa", "La Emperatriz", "El Emperador", 
    "El Hierofante", "Los Enamorados", "El Carro", "La Justicia", "El Ermitano", 
    "La Rueda de la Fortuna", "La Fuerza", "El Colgado", "La Muerte", 
    "La Templanza", "El Diablo", "La Torre", "La Estrella", "La Luna", "El Sol", 
    "El Juicio", "El Mundo"
] + [f"{face} de {suit}" for suit in ["Copas", "Oros", "Espadas", "Bastos"]
     for face in ["As", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve", "Diez", "Sota", "Caballo","Reina","Rey"]]

def draw_cards(count):
    chosen = random.sample(TAROT_CARDS, count)
    return [{"name": name, "position": random.choice(["derecha", "invertida"])} for name in chosen]
