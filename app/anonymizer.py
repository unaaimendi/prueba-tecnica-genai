import re

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b(?:\+?\d{1,3})?[-.\s]?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b",
    "dni": r"\b\d{7,8}[A-Za-z]\b",
    "name": r"\b[A-Z][a-z]{1,30}(?:\s[A-Z][a-z]{1,30})+\b"
}

REPLACEMENTS = {
    "email": "[email]",
    "phone": "[phone]",
    "dni": "[id]",
    "name": "[name]"
}

def anonymize(text: str) -> str:
    for key, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, REPLACEMENTS[key], text)
    return text
