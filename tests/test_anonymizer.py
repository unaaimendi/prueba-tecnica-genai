from app.anonymizer import anonymize_text

def test_anonymization():
    input_text = "Llamó Juan Pérez desde Madrid y dejó su número 600123456."
    anonymized = anonymize_text(input_text)
    assert "<PERSON>" in anonymized or "<GPE>" in anonymized or "<PHONE>" in anonymized
