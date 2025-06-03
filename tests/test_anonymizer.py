import pytest
from app.anonymizer import anonymize

@pytest.mark.parametrize("input_text, expected", [
    # Email
    ("Contacta a juan.perez@example.com", "Contacta a [email]"),
    ("Emails: test123@dominio.es y otro@correo.com", "Emails: [email] y [email]"),

    # Teléfonos
    ("Mi número es 123-456-789", "Mi número es [phone]"),
    ("Llama al 912 345 678", "Llama al [phone]"),

    # DNI
    ("El cliente tiene DNI 12345678Z", "El cliente tiene DNI [id]"),

    # Nombres (nombres compuestos)
    ("Nombre completo: Juan Pérez", "Nombre completo: [name]"),
    ("Responsable: María del Carmen García López", "Responsable: [name]"),

    # Combinado
    ("Juan Pérez con DNI 12345678Z y email juan.perez@correo.com",
     "[name] con DNI [id] y email [email]"),

    # Sin datos PII
    ("El sistema está caído desde las 10 AM", "El sistema está caído desde las 10 AM"),

    # Texto vacío
    ("", ""),
])

def test_anonymizer(input_text, expected):
    assert anonymize(input_text) == expected
