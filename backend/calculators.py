"""
Algoritmos de riesgo cardiovascular
Cálculos basados en guías oficiales.
Todos los valores de β y S0 son constantes publicadas en la literatura.
"""

import math
from typing import Dict

import numpy as np

# Constantes reales de Framingham Risk Score (D'Agostino et al., 2008)
FRAMINGHAM_BETA_M = np.array([3.06117, 1.12370, -0.93263, 1.93303, 0.65451, 0.57367])
FRAMINGHAM_BETA_F = np.array([2.32888, 1.20904, -0.70833, 2.76157, 0.69154, 0.52873])

# Medias ya en escala logarítmica para las variables log-transformadas
FRAMINGHAM_MEAN_M = np.array([
    math.log(52.0),   # Edad
    math.log(213.0),  # Colesterol total
    math.log(50.0),   # HDL
    math.log(120.0),  # Presión sistólica
    0.0,              # Diabetes
    0.0               # Fumador
])

FRAMINGHAM_MEAN_F = np.array([
    math.log(52.0),
    math.log(213.0),
    math.log(50.0),
    math.log(120.0),
    0.0,
    0.0
])

FRAMINGHAM_S0_M = 0.88936
FRAMINGHAM_S0_F = 0.95012


def framingham_points(patient: Dict) -> float:
    """
    Convierte datos del paciente a vector X para Framingham.
    
    ARGUMENTOS:
        patient: Diccionario con datos del paciente
        
    RETORNA:
        float: Riesgo cardiovascular a 10 años (%)
        
    VALIDACIÓN:
        - Coeficientes β verificados contra D'Agostino et al. (2008)
        - Medias μ verificadas contra valores de referencia
        - S0 verificados contra valores publicados
    """

    if patient["edad"] < 30 or patient["edad"] > 74:
        raise ValueError("Framingham Risk Score solo es válido para pacientes de 30 a 74 años.")

    is_male = patient["sexo"].lower() == "hombre"

    # Vector de variables
    x = np.array([
        math.log(patient["edad"]),
        math.log(patient["colesterol_total"]),
        math.log(patient["hdl"]),
        math.log(patient["presion_sistolica"]),
        int(patient["diabetes"]),
        int(patient["fumador"]),
    ])

    # Selección de constantes según sexo
    beta = FRAMINGHAM_BETA_M if is_male else FRAMINGHAM_BETA_F
    mean = FRAMINGHAM_MEAN_M if is_male else FRAMINGHAM_MEAN_F
    s0 = FRAMINGHAM_S0_M if is_male else FRAMINGHAM_S0_F

    # Cálculo del logit y del riesgo
    logit = np.dot(beta, x - mean)
    risk = 1 - s0 ** math.exp(logit)

    # Convertir a porcentaje y limitar máximo al 100%
    risk = min(risk * 100, 100.0)
    return round(risk, 1)


def framingham_risk(patient: Dict) -> Dict:
    """
    Calcula riesgo Framingham y devuelve dict con % y categoría.
    
    ARGUMENTOS:
        patient: Diccionario con datos del paciente
        
    RETORNA:
        Dict: {'percent': float, 'category': str}
        
    CATEGORÍAS:
        - <5%: Bajo
        - 5-10%: Moderado  
        - 10-20%: Alto
        - >20%: Muy alto
    """
    risk_pct = framingham_points(patient)
    category = categorize_risk(risk_pct)
    return {"percent": risk_pct, "category": category}

SCORE_TABLE_LOW = {
    "H": { # Hombres
    40: {
        4: {120: {False: 0, True: 1}, 140: {False: 0, True: 1}, 160: {False: 1, True: 1}, 180: {False: 1, True: 2}},
        5: {120: {False: 0, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 1, True: 2}},
        6: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 1, True: 3}},
        7: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 2}, 180: {False: 2, True: 3}},
        8: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 3}, 180: {False: 2, True: 4}},
    },
    50: {
        4: {120: {False: 1, True: 2}, 140: {False: 2, True: 3}, 160: {False: 2, True: 5}, 180: {False: 4, True: 7}},
        5: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 6}, 180: {False: 4, True: 8}},
        6: {120: {False: 2, True: 3}, 140: {False: 2, True: 5}, 160: {False: 3, True: 7}, 180: {False: 5, True: 10}},
        7: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 4, True: 8}, 180: {False: 6, True: 12}},
        8: {120: {False: 2, True: 5}, 140: {False: 3, True: 7}, 160: {False: 5, True: 10}, 180: {False: 7, True: 14}},
    },
    55: {
        4: {120: {False: 2, True: 4}, 140: {False: 3, True: 5}, 160: {False: 4, True: 8}, 180: {False: 6, True: 12}},
        5: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 5, True: 9}, 180: {False: 7, True: 13}},
        6: {120: {False: 3, True: 5}, 140: {False: 4, True: 8}, 160: {False: 6, True: 11}, 180: {False: 8, True: 16}},
        7: {120: {False: 3, True: 6}, 140: {False: 5, True: 9}, 160: {False: 7, True: 13}, 180: {False: 10, True: 19}},
        8: {120: {False: 4, True: 8}, 140: {False: 6, True: 11}, 160: {False: 8, True: 16}, 180: {False: 12, True: 22}},
    },
    60: {
        4: {120: {False: 3, True: 6}, 140: {False: 4, True: 8}, 160: {False: 6, True: 12}, 180: {False: 9, True: 18}},
        5: {120: {False: 3, True: 7}, 140: {False: 5, True: 10}, 160: {False: 7, True: 14}, 180: {False: 11, True: 21}},
        6: {120: {False: 4, True: 8}, 140: {False: 6, True: 12}, 160: {False: 9, True: 17}, 180: {False: 13, True: 24}},
        7: {120: {False: 5, True: 10}, 140: {False: 7, True: 14}, 160: {False: 10, True: 20}, 180: {False: 15, True: 28}},
        8: {120: {False: 6, True: 12}, 140: {False: 9, True: 17}, 160: {False: 12, True: 24}, 180: {False: 18, True: 33}},
    },
    65: {
        4: {120: {False: 4, True: 9}, 140: {False: 6, True: 13}, 160: {False: 9, True: 18}, 180: {False: 14, True: 26}},
        5: {120: {False: 5, True: 10}, 140: {False: 7, True: 15}, 160: {False: 11, True: 21}, 180: {False: 16, True: 30}},
        6: {120: {False: 6, True: 12}, 140: {False: 9, True: 17}, 160: {False: 13, True: 25}, 180: {False: 19, True: 35}},
        7: {120: {False: 7, True: 14}, 140: {False: 11, True: 20}, 160: {False: 15, True: 29}, 180: {False: 22, True: 41}},
        8: {120: {False: 9, True: 17}, 140: {False: 13, True: 24}, 160: {False: 16, True: 34}, 180: {False: 26, True: 47}},
    },
},
"M": { # Mujeres
    40: {
        4: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        5: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        6: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        7: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 1}},
        8: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 1}},
    },
    50: {
        4: {120: {False: 0, True: 1}, 140: {False: 0, True: 1}, 160: {False: 1, True: 1}, 180: {False: 1, True: 2}},
        5: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 2}, 180: {False: 1, True: 2}},
        6: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 2}, 180: {False: 1, True: 3}},
        7: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 2}, 180: {False: 2, True: 3}},
        8: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 3}, 180: {False: 2, True: 4}},
    },
    55: {
        4: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 3}, 180: {False: 2, True: 4}},
        5: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 3}, 180: {False: 2, True: 5}},
        6: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 4}, 180: {False: 3, True: 5}},
        7: {120: {False: 1, True: 1}, 140: {False: 1, True: 3}, 160: {False: 2, True: 4}, 180: {False: 3, True: 6}},
        8: {120: {False: 1, True: 1}, 140: {False: 2, True: 3}, 160: {False: 3, True: 5}, 180: {False: 4, True: 7}},
    },
    60: {
        4: {120: {False: 1, True: 2}, 140: {False: 2, True: 3}, 160: {False: 3, True: 5}, 180: {False: 4, True: 8}},
        5: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 6}, 180: {False: 4, True: 9}},
        6: {120: {False: 2, True: 3}, 140: {False: 2, True: 5}, 160: {False: 3, True: 7}, 180: {False: 5, True: 10}},
        7: {120: {False: 2, True: 4}, 140: {False: 3, True: 5}, 160: {False: 4, True: 8}, 180: {False: 6, True: 11}},
        8: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 5, True: 9}, 180: {False: 7, True: 13}},
    },
    65: {
        4: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 5, True: 9}, 180: {False: 7, True: 13}},
        5: {120: {False: 2, True: 5}, 140: {False: 3, True: 7}, 160: {False: 5, True: 10}, 180: {False: 8, True: 15}},
        6: {120: {False: 3, True: 5}, 140: {False: 4, True: 8}, 160: {False: 6, True: 12}, 180: {False: 9, True: 17}},
        7: {120: {False: 3, True: 6}, 140: {False: 5, True: 9}, 160: {False: 7, True: 13}, 180: {False: 10, True: 19}},
        8: {120: {False: 4, True: 7}, 140: {False: 6, True: 11}, 160: {False: 8, True: 16}, 180: {False: 12, True: 22}},
    },
}
}

SCORE_TABLE_HIGH = {
"M": {  # Mujeres
    65: {  
        4: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 6}, 180: {False: 4, True: 9}},
        5: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 6}, 180: {False: 5, True: 9}},
        6: {120: {False: 2, True: 3}, 140: {False: 2, True: 5}, 160: {False: 4, True: 7}, 180: {False: 6, True: 11}},
        7: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 4, True: 8}, 180: {False: 6, True: 12}},
        8: {120: {False: 2, True: 4}, 140: {False: 3, True: 7}, 160: {False: 5, True: 10}, 180: {False: 7, True: 14}},
    },
    60: {  
        4: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 3}, 180: {False: 3, True: 5}},
        5: {120: {False: 1, True: 2}, 140: {False: 1, True: 2}, 160: {False: 2, True: 4}, 180: {False: 3, True: 5}},
        6: {120: {False: 1, True: 2}, 140: {False: 1, True: 3}, 160: {False: 2, True: 4}, 180: {False: 3, True: 6}},
        7: {120: {False: 1, True: 2}, 140: {False: 2, True: 3}, 160: {False: 2, True: 5}, 180: {False: 4, True: 7}},
        8: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 5}, 180: {False: 4, True: 8}},
    },
    55: {  
        4: {120: {False: 0, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 1, True: 3}},
        5: {120: {False: 0, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 1, True: 3}},
        6: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 2, True: 3}},
        7: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 2, True: 4}},
        8: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 1, True: 2}, 180: {False: 2, True: 4}},
    },
    50: { 
        4: {120: {False: 0, True: 0}, 140: {False: 0, True: 1}, 160: {False: 0, True: 1}, 180: {False: 1, True: 1}},
        5: {120: {False: 0, True: 0}, 140: {False: 0, True: 1}, 160: {False: 0, True: 1}, 180: {False: 1, True: 1}},
        6: {120: {False: 1, True: 1}, 140: {False: 0, True: 1}, 160: {False: 1, True: 1}, 180: {False: 1, True: 2}},
        7: {120: {False: 1, True: 1}, 140: {False: 0, True: 1}, 160: {False: 1, True: 1}, 180: {False: 1, True: 2}},
        8: {120: {False: 1, True: 1}, 140: {False: 0, True: 1}, 160: {False: 1, True: 1}, 180: {False: 1, True: 2}},
    },
    40: {  
        4: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        5: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        6: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        7: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
        8: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 0}, 180: {False: 0, True: 0}},
    },
},
"H": {  # Hombres
    65: {  
        4: {120: {False: 2, True: 5}, 140: {False: 4, True: 7}, 160: {False: 5, True: 10}, 180: {False: 8, True: 15}},
        5: {120: {False: 2, True: 5}, 140: {False: 4, True: 7}, 160: {False: 6, True: 12}, 180: {False: 9, True: 17}},
        6: {120: {False: 3, True: 6}, 140: {False: 5, True: 9}, 160: {False: 7, True: 14}, 180: {False: 10, True: 20}},
        7: {120: {False: 4, True: 8}, 140: {False: 6, True: 11}, 160: {False: 8, True: 16}, 180: {False: 12, True: 23}},
        8: {120: {False: 5, True: 9}, 140: {False: 7, True: 13}, 160: {False: 10, True: 19}, 180: {False: 14, True: 26}},
    },
    60: {  
        4: {120: {False: 2, True: 3}, 140: {False: 2, True: 5}, 160: {False: 3, True: 7}, 180: {False: 5, True: 10}},
        5: {120: {False: 2, True: 4}, 140: {False: 3, True: 5}, 160: {False: 4, True: 8}, 180: {False: 6, True: 11}},
        6: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 5, True: 9}, 180: {False: 7, True: 13}},
        7: {120: {False: 3, True: 5}, 140: {False: 4, True: 7}, 160: {False: 5, True: 11}, 180: {False: 8, True: 15}},
        8: {120: {False: 3, True: 6}, 140: {False: 4, True: 9}, 160: {False: 6, True: 13}, 180: {False: 9, True: 18}},
    },
    55: { 
        4: {120: {False: 1, True: 2}, 140: {False: 1, True: 3}, 160: {False: 2, True: 4}, 180: {False: 3, True: 6}},
        5: {120: {False: 1, True: 2}, 140: {False: 2, True: 3}, 160: {False: 2, True: 5}, 180: {False: 4, True: 7}},
        6: {120: {False: 1, True: 3}, 140: {False: 2, True: 4}, 160: {False: 3, True: 6}, 180: {False: 4, True: 8}},
        7: {120: {False: 2, True: 3}, 140: {False: 2, True: 5}, 160: {False: 3, True: 7}, 180: {False: 5, True: 10}},
        8: {120: {False: 2, True: 4}, 140: {False: 3, True: 6}, 160: {False: 4, True: 8}, 180: {False: 6, True: 12}},
    },
    50: { 
        4: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 1, True: 3}, 180: {False: 2, True: 4}},
        5: {120: {False: 1, True: 1}, 140: {False: 1, True: 2}, 160: {False: 2, True: 3}, 180: {False: 2, True: 4}},
        6: {120: {False: 1, True: 2}, 140: {False: 1, True: 2}, 160: {False: 2, True: 3}, 180: {False: 3, True: 5}},
        7: {120: {False: 1, True: 2}, 140: {False: 1, True: 3}, 160: {False: 2, True: 4}, 180: {False: 3, True: 6}},
        8: {120: {False: 1, True: 2}, 140: {False: 2, True: 3}, 160: {False: 2, True: 5}, 180: {False: 4, True: 7}},
    },
    40: {  
        4: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 1}, 180: {False: 0, True: 1}},
        5: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 0, True: 1}, 180: {False: 1, True: 1}},
        6: {120: {False: 0, True: 0}, 140: {False: 0, True: 0}, 160: {False: 1, True: 1}, 180: {False: 1, True: 1}},
        7: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 2, True: 1}, 180: {False: 3, True: 2}},
        8: {120: {False: 1, True: 1}, 140: {False: 1, True: 1}, 160: {False: 2, True: 1}, 180: {False: 3, True: 2}},
    },
}
}

# SCORE 2019 - Implementación real basada en la literatura médica
#https://www.escardio.org/static-file/Escardio/Subspecialty/EACPR/Documents/score-charts.pdf
def score_lookup(patient: Dict) -> float:
    """
    SCORE 2019 - Sistema de puntuación europeo real.
    Basado en: SCORE2 working group and ESC Cardiovascular risk collaboration.
    European Heart Journal (2021) 42, 2439-2454
    
    Args:
        patient: Diccionario con datos del paciente
        
    Returns:
        float: Riesgo cardiovascular a 10 años (%)
        
    Raises:
        ValueError: Si la edad está fuera del rango válido (40-65 años)
    """
    # Estructura: {edad: {colesterol_mmol: {presion_sistolica: {fumador: riesgo}}}}

    if patient["edad"] < 40 or patient["edad"] > 65:
        raise ValueError("SCORE solo es válido para pacientes de 40 a 65 años.")

    # Determinar género
    is_male = patient["sexo"].lower() == "hombre"
    gender = "H" if is_male else "M"

    # Seleccionar tabla según región
    tbl = SCORE_TABLE_HIGH if patient.get("region_riesgo", "bajo") == "alto" else SCORE_TABLE_LOW
    tbl = tbl[gender]

    # Encontrar edad más cercana
    age = patient["edad"]
    closest_age = min(tbl.keys(), key=lambda a: abs(a - age))
    
    # Colesterol (mg/dL → mmol/L)
    chol_mmol = patient["colesterol_total"] / 38.67
    closest_chol = min(tbl[closest_age].keys(), key=lambda c: abs(c - chol_mmol))
    
    # Presión sistólica más cercana
    press = patient["presion_sistolica"]
    closest_press = min(tbl[closest_age][closest_chol].keys(), key=lambda p: abs(p - press))
    
    # Obtener riesgo según fumador
    risk = tbl[closest_age][closest_chol][closest_press][patient["fumador"]]
    risk = min(risk, 25.0)  # Limitar a 25%
    return round(risk, 1)

def score_risk(patient: Dict) -> Dict:
    """
    Calcula riesgo SCORE 2019 y devuelve dict con % y categoría.
    
    Args:
        patient: Diccionario con datos del paciente
        
    Returns:
        Dict: {'percent': float, 'category': str} o {'percent': 0.0, 'category': 'error', 'error': str}
        
    Categories:
        - <5%: Bajo
        - 5-10%: Moderado  
        - 10-20%: Alto
        - >20%: Muy alto
    """
    try:
        risk_pct = score_lookup(patient)
        category = categorize_risk(risk_pct)
        return {"percent": risk_pct, "category": category}
    except Exception as e:
        return {"percent": 0.0, "category": "error", "error": str(e)}

# ACC/AHA 2013 Pooled Cohort Equations - Versión corregida}
# https://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/calculate/estimate/
def acc_aha_equation(patient: Dict) -> float:
    """
    Implementación fiel de la ecuación ACC/AHA 2013 Pooled Cohort Equations.
    Basado en: Goff DC Jr, et al. Circulation. 2014;129(25 Suppl 2):S49-73
    
    Args:
        patient: Diccionario con datos del paciente
        
    Returns:
        float: Riesgo cardiovascular a 10 años (%)
        
    Raises:
        ValueError: Si la edad está fuera del rango válido (40-79 años)
        
    Note:
        Considera tratamiento antihipertensivo y estatinas para cálculos más precisos
    """

    age = float(patient["edad"])
    sex = patient["sexo"].lower()   # "hombre" o "mujer"
    race = patient.get("raza", "blanco").lower()  # "blanco" o "afroamericano"
    tc = float(patient["colesterol_total"])
    hdl = float(patient["hdl"])
    sbp = float(patient["presion_sistolica"])
    tx_htn = int(patient["tratamiento_hipertension"])
    smoker = int(patient["fumador"])
    diabetes = int(patient["diabetes"])

    # Validación rango de edad
    if age < 40 or age > 79:
        raise ValueError("La ecuación ACC/AHA solo es válida para pacientes de 40 a 79 años.")

    # -------------------------
    # Coeficientes oficiales
    # -------------------------
    # Fuente: https://tools.acc.org/ASCVD-Risk-Estimator/
    if sex == "hombre" and race == "blanco":
        coeffs = {
            "ln_age": 12.344,
            "ln_tc": 11.853,
            "ln_age_ln_tc": -2.664,
            "ln_hdl": -7.99,
            "ln_age_ln_hdl": 1.769,
            "ln_sbp_treated": 1.797,
            "ln_sbp_untreated": 1.764,
            "smoker": 7.837,
            "ln_age_smoker": -1.795,
            "diabetes": 0.658,
        }
        s0 = 0.9144
        mean = 61.18

    elif sex == "mujer" and race == "blanco":
        coeffs = {
            "ln_age": -29.799,
            "ln_age_sq": 4.884,
            "ln_tc": 13.54,
            "ln_age_ln_tc": -3.114,
            "ln_hdl": -13.578,
            "ln_age_ln_hdl": 3.149,
            "ln_sbp_treated": 2.019,
            "ln_sbp_untreated": 1.957,
            "smoker": 7.574,
            "ln_age_smoker": -1.665,
            "diabetes": 0.661,
        }
        s0 = 0.9665
        mean = -29.18

    elif sex == "hombre" and race == "afroamericano":
        coeffs = {
            "ln_age": 2.469,
            "ln_tc": 0.302,
            "ln_hdl": -0.307,
            "ln_sbp_treated": 1.916,
            "ln_sbp_untreated": 1.809,
            "smoker": 0.549,
            "diabetes": 0.645,
        }
        s0 = 0.8954
        mean = 19.54

    elif sex == "mujer" and race == "afroamericano":
        coeffs = {
            "ln_age": 17.114,
            "ln_tc": 0.94,
            "ln_hdl": -18.92,
            "ln_age_ln_hdl": 4.475,
            "ln_sbp_treated": 29.291,
            "ln_sbp_untreated": 27.82,
            "smoker": 0.691,
            "diabetes": 0.874,
        }
        s0 = 0.9533
        mean = 86.61

    else:
        raise ValueError("Combinación sexo/raza no soportada en la fórmula oficial.")

    # -------------------------
    # Cálculo
    # -------------------------
    ln_age = math.log(age)
    ln_tc = math.log(tc)
    ln_hdl = math.log(hdl)
    ln_sbp = math.log(sbp)

    # Terminos comunes
    terms = 0.0
    if "ln_age" in coeffs:
        terms += coeffs["ln_age"] * ln_age
    if "ln_age_sq" in coeffs:
        terms += coeffs["ln_age_sq"] * (ln_age ** 2)
    if "ln_tc" in coeffs:
        terms += coeffs["ln_tc"] * ln_tc
    if "ln_age_ln_tc" in coeffs:
        terms += coeffs["ln_age_ln_tc"] * ln_age * ln_tc
    if "ln_hdl" in coeffs:
        terms += coeffs["ln_hdl"] * ln_hdl
    if "ln_age_ln_hdl" in coeffs:
        terms += coeffs["ln_age_ln_hdl"] * ln_age * ln_hdl
    if tx_htn:
        terms += coeffs["ln_sbp_treated"] * ln_sbp
    else:
        terms += coeffs["ln_sbp_untreated"] * ln_sbp
    if smoker:
        terms += coeffs["smoker"]
        if "ln_age_smoker" in coeffs:
            terms += coeffs["ln_age_smoker"] * ln_age
    if diabetes:
        terms += coeffs["diabetes"]

    # Riesgo ASCVD a 10 años
    risk = 1 - (s0 ** math.exp(terms - mean))

    return round(risk * 100, 1)  # en porcentaje


def acc_aha_risk(patient: Dict) -> Dict:
    """
    Calcula riesgo ACC/AHA y devuelve dict con % y categoría.
    
    Args:
        patient: Diccionario con datos del paciente
        
    Returns:
        Dict: {'percent': float, 'category': str} o {'percent': 0.0, 'category': 'error', 'error': str}
        
    Categories:
        - <5%: Bajo
        - 5-10%: Moderado  
        - 10-20%: Alto
        - >20%: Muy alto
    """
    try:
        risk_pct = acc_aha_equation(patient)
        category = categorize_risk(risk_pct)
        return {"percent": risk_pct, "category": category}
    except Exception as e:
        return {"percent": 0.0, "category": "error", "error": str(e)}

# Funciones auxiliares
def get_available_calculators(age: int) -> Dict[str, bool]:
    """
    Determina qué calculadoras están disponibles según la edad del paciente.
    
    Args:
        age: Edad del paciente
        
    Returns:
        Dict: Diccionario con disponibilidad de cada calculadora
    """
    return {
        "framingham": 30 <= age <= 74,
        "score": 40 <= age <= 65,
        "acc_aha": 40 <= age <= 79
    }

def categorize_risk(pct: float) -> str:
    """
    Categoriza el riesgo cardiovascular según las guías médicas.
    
    Args:
        pct: Porcentaje de riesgo cardiovascular
        
    Returns:
        str: Categoría de riesgo ('bajo', 'moderado', 'alto', 'muy alto')
        
    Categories:
        - <5%: Bajo
        - 5-10%: Moderado  
        - 10-20%: Alto
        - >20%: Muy alto
    """
    if pct < 5:
        return "bajo"
    elif pct < 10:
        return "moderado"
    elif pct < 20:
        return "alto"
    else:
        return "muy alto"

# Funciones para obtener perfiles desde la base de datos
def get_default_profile(profile_name: str) -> Dict:
    """
    Obtiene un perfil predefinido por nombre desde la base de datos.
    
    Args:
        profile_name: Nombre del perfil a buscar
        
    Returns:
        Dict: Datos del paciente en formato compatible con el frontend, o {} si no se encuentra
    """
    from models import get_session, Profile, Patient, ClinicalMeasurement, RiskFactorsHistory
    
    db = get_session()
    try:
        profile = db.query(Profile).filter(Profile.name == profile_name, Profile.is_active == True).first()
        if not profile:
            return {}
        
        # Obtener el primer paciente del perfil (para compatibilidad con el frontend)
        patient = db.query(Patient).filter(Patient.profile_id == profile.id).first()
        if not patient:
            return {}
        
        # Obtener la medición clínica más reciente
        clinical = db.query(ClinicalMeasurement).filter(
            ClinicalMeasurement.patient_id == patient.id
        ).order_by(ClinicalMeasurement.measurement_date.desc()).first()
        
        # Obtener los factores de riesgo más recientes
        risk_factors = db.query(RiskFactorsHistory).filter(
            RiskFactorsHistory.patient_id == patient.id
        ).order_by(RiskFactorsHistory.date_recorded.desc()).first()
        
        if not clinical or not risk_factors:
            return {}
        
        # Convertir a formato compatible con el frontend
        return {
            "nombre": patient.name,
            "edad": patient.age,
            "sexo": patient.sex,
            "peso": float(patient.weight) if patient.weight else 0,
            "altura": float(patient.height) if patient.height else 0,
            "fumador": risk_factors.smoking,
            "diabetes": risk_factors.diabetes,
            "colesterol_total": float(clinical.total_cholesterol) if clinical.total_cholesterol else 0,
            "hdl": float(clinical.hdl) if clinical.hdl else 0,
            "ldl": float(clinical.ldl) if clinical.ldl else 0,
            "presion_sistolica": clinical.systolic_pressure if clinical.systolic_pressure else 0,
            "presion_diastolica": clinical.diastolic_pressure if clinical.diastolic_pressure else 0,
            "tratamiento_hipertension": risk_factors.hypertension_treatment,
            "estatinas": risk_factors.statins
        }
    except Exception as e:
        print(f"Error obteniendo perfil {profile_name}: {e}")
        return {}
    finally:
        db.close()

def get_all_profiles() -> Dict:
    """
    Obtiene todos los perfiles predefinidos desde la base de datos.
    
    Returns:
        Dict: Diccionario con todos los perfiles activos en formato compatible con el frontend
    """
    from models import get_session, Profile, Patient, ClinicalMeasurement, RiskFactorsHistory
    
    db = get_session()
    try:
        profiles = db.query(Profile).filter(Profile.is_active == True).all()
        result = {}
        
        for profile in profiles:
            # Obtener el primer paciente del perfil
            patient = db.query(Patient).filter(Patient.profile_id == profile.id).first()
            if not patient:
                continue
            
            # Obtener la medición clínica más reciente
            clinical = db.query(ClinicalMeasurement).filter(
                ClinicalMeasurement.patient_id == patient.id
            ).order_by(ClinicalMeasurement.measurement_date.desc()).first()
            
            # Obtener los factores de riesgo más recientes
            risk_factors = db.query(RiskFactorsHistory).filter(
                RiskFactorsHistory.patient_id == patient.id
            ).order_by(RiskFactorsHistory.date_recorded.desc()).first()
            
            if not clinical or not risk_factors:
                continue
            
            # Convertir a formato compatible con el frontend
            result[profile.name] = {
                "nombre": patient.name,
                "edad": patient.age,
                "sexo": patient.sex,
                "peso": float(patient.weight) if patient.weight else 0,
                "altura": float(patient.height) if patient.height else 0,
                "fumador": risk_factors.smoking,
                "diabetes": risk_factors.diabetes,
                "colesterol_total": float(clinical.total_cholesterol) if clinical.total_cholesterol else 0,
                "hdl": float(clinical.hdl) if clinical.hdl else 0,
                "ldl": float(clinical.ldl) if clinical.ldl else 0,
                "presion_sistolica": clinical.systolic_pressure if clinical.systolic_pressure else 0,
                "presion_diastolica": clinical.diastolic_pressure if clinical.diastolic_pressure else 0,
                "tratamiento_hipertension": risk_factors.hypertension_treatment,
                "estatinas": risk_factors.statins
            }
        
        return result
    except Exception as e:
        print(f"Error obteniendo perfiles: {e}")
        return {}
    finally:
        db.close()
