def build_prompt(cards, spread_type):
    spread_names = {
        1: "Tirada de 1 carta (Consejo o respuesta rápida)",
        3: "Tirada de 3 cartas (Pasado, Presente, Futuro)",
        7: "Tirada en herradura (Evaluación general)",
        10: "Cruz Celta (Análisis profundo)"
    }

    prompt_lines = [
        f"Lectura de tarot - {spread_type} cartas: {spread_names.get(spread_type, 'Tirada desconocida')}",
        "A continuación, las cartas y su posición en la tirada:\n"
    ]

    for idx, card in enumerate(cards, 1):
        orientation = "invertida" if card.get("reversed", False) else "derecha"
        position = card.get("position", "posición desconocida")
        prompt_lines.append(f"{idx}. {card['name']} - {position} ({orientation})")

    prompt_lines.append(
        "\nEres una tarotista con profunda sabiduría espiritual. Interpreta cada carta considerando su nombre, "
        "posición, orientación y las conexiones entre ellas. Ofrece una lectura introspectiva, clara y enriquecedora "
        "que guíe espiritualmente al consultante."
    )

    return "\n".join(prompt_lines)