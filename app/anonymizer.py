import re
import spacy

# Carga el modelo de lenguaje spaCy
nlp = spacy.load("es_core_news_md")

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # correos electrónicos
    "phone": r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b",  # números de teléfono
    "dni": r"\b\d{7,8}[A-Za-z]\b"  # DNI español
}

REPLACEMENTS = {
    "email": "[email]",
    "phone": "[phone]",
    "dni": "[id]",
    "name": "[name]"
}

def anonymize(text: str) -> str:
    """
    Anonimiza un texto eliminando información personal identificable (PII), como correos electrónicos,
    números de teléfono, DNI y nombres propios.

    Args:
        text (str): Texto de entrada que puede contener datos sensibles.

    Returns:
        str: Texto anonimizado en el que las entidades PII han sido reemplazadas por etiquetas como
             [email], [phone], [id] y [name].
    """
    # Reemplazar patrones
    for key, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, REPLACEMENTS[key], text)

    # Detectar nombres propios y otras entidades
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in {"PER", "ORG", "LOC"}:
            text = text.replace(ent.text, REPLACEMENTS["name"])

    return text
