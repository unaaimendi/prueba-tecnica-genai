import json
from pathlib import Path
from app.schemas import Department, Case

DATA_DIR = Path(__file__).parent.parent / "data"


def load_departments() -> list[Department]:
    """
    Carga los departamentos desde el archivo JSON 'departments.json'.

    Returns:
        list[Department]: Lista de objetos Department deserializados desde el archivo.
    """
    with open(DATA_DIR / "departments.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Department(**d) for d in data]


def load_cases() -> list[Case]:
    """
    Carga los casos desde el archivo JSON 'cases.json'.

    Returns:
        list[Case]: Lista de objetos Case deserializados desde el archivo.
    """
    with open(DATA_DIR / "cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Case(**c) for c in data]
