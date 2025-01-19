def normalize_text(text):
    replacements = {
        "fouled": "foul",
        "substitute": "substituted",
        "substitution": "substituted",
        "susbstituted": "substituted",
        "goaled": "goal",
        "goals": "goal",
        "assistes": "assisted",
        "assist": "assisted",
        "gold": "goal"
    }
    for word, replacement in replacements.items():
        text = text.replace(word, replacement)
    return text