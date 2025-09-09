"""
Validación de datos clínicos y advertencias médicas
"""

from typing import Tuple, List, Dict

RANGES = {
    "edad": (20, 79),
    "presion_sistolica": (90, 200),
    "colesterol_total": (100, 400),
    "hdl": (20, 100),
    "ldl": (50, 200),
    "presion_diastolica": (60, 120),
    "peso": (30, 200),
    "altura": (100, 250),
}

def validate_patient_data(data: Dict) -> Tuple[bool, List[str]]:
    """
    Devuelve (True, warnings) si es válido o (False, errors) si hay errores.
    """
    errors, warnings = [], []

    # Validar campos obligatorios
    required_fields = ["edad", "sexo", "colesterol_total", "hdl", "presion_sistolica"]
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"Falta el parámetro obligatorio: {field}")
            continue
        
        if field in RANGES:
            value = float(data[field])
            low, high = RANGES[field]
            if not (low <= value <= high):
                errors.append(f"{field} fuera de rango ({low}-{high}): {value}")
            elif value in (low, high):
                warnings.append(f"{field} en el límite permitido: {value}")

    # Validar sexo
    if "sexo" in data and data["sexo"] not in ["hombre", "mujer"]:
        errors.append("Sexo debe ser 'hombre' o 'mujer'")

    # Campos booleanos obligatorios
    bool_fields = ["fumador", "diabetes", "tratamiento_hipertension", "estatinas"]
    for bf in bool_fields:
        if bf not in data:
            data[bf] = False  # Valor por defecto
        elif not isinstance(data[bf], bool):
            data[bf] = bool(data[bf])

    # Validaciones médicas específicas
    if "edad" in data and "presion_sistolica" in data:
        edad = float(data["edad"])
        presion = float(data["presion_sistolica"])
        if edad < 40 and presion > 140:
            warnings.append("Presión sistólica elevada para la edad")
        if edad > 65 and presion > 130:
            warnings.append("Presión sistólica elevada para la edad")

    if "colesterol_total" in data and "hdl" in data:
        col_total = float(data["colesterol_total"])
        hdl = float(data["hdl"])
        if col_total / hdl > 5:
            warnings.append("Ratio colesterol total/HDL elevado (>5)")

    return (len(errors) == 0, errors if errors else warnings)
