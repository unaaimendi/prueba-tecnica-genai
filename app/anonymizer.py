import re
import spacy

# Para detección de entidades nombradas
nlp = spacy.load("es_core_news_md")  # para español

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b",
    "dni": r"\b\d{7,8}[A-Za-z]\b"
}

REPLACEMENTS = {
    "email": "[email]",
    "phone": "[phone]",
    "dni": "[id]",
    "name": "[name]"
}

def anonymize(text: str) -> str:
    # Paso 1: patrones regulares
    for key, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, REPLACEMENTS[key], text)

    # Paso 2: usar spaCy para detectar nombres propios y entidades
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in {"PER", "ORG", "LOC"}:  # personas, organizaciones, lugares
            text = text.replace(ent.text, REPLACEMENTS["name"])

    return text
