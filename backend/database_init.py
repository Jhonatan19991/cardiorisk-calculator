"""
Script para inicializar la base de datos con perfiles predefinidos
"""

from models import (
    Profile, Patient, ClinicalMeasurement, RiskFactorsHistory,
    get_session, create_tables
)
from datetime import datetime

def init_database():
    """Inicializa la base de datos y crea perfiles predefinidos"""
    print("📊 Creando tablas en la base de datos...")
    try:
        create_tables()
        print("✅ Tablas creadas correctamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        raise
    
    print("👥 Creando perfiles predefinidos...")
    # Crear perfiles predefinidos
    profiles_data = [
        {
            "name": "joven_sano",
            "description": "Perfil de joven sano sin factores de riesgo",
            "patients": [
                {
                    "name": "Joven Sano",
                    "age": 30,
                    "sex": "hombre",
                    "weight": 70.0,
                    "height": 175.0,
                    "clinical": {
                        "total_cholesterol": 180.0,
                        "hdl": 55.0,
                        "ldl": 110.0,
                        "systolic_pressure": 120,
                        "diastolic_pressure": 80
                    },
                    "risk_factors": {
                        "smoking": False,
                        "diabetes": False,
                        "hypertension_treatment": False,
                        "statins": False
                    }
                }
            ]
        },
        {
            "name": "adulto_riesgo_moderado",
            "description": "Perfil de adulto con riesgo moderado",
            "patients": [
                {
                    "name": "Adulto Riesgo Moderado",
                    "age": 55,
                    "sex": "hombre",
                    "weight": 85.0,
                    "height": 170.0,
                    "clinical": {
                        "total_cholesterol": 220.0,
                        "hdl": 45.0,
                        "ldl": 140.0,
                        "systolic_pressure": 145,
                        "diastolic_pressure": 90
                    },
                    "risk_factors": {
                        "smoking": True,
                        "diabetes": False,
                        "hypertension_treatment": False,
                        "statins": False
                    }
                }
            ]
        },
        {
            "name": "adulta_diabetica",
            "description": "Perfil de adulta diabética",
            "patients": [
                {
                    "name": "Adulta Diabética",
                    "age": 65,
                    "sex": "mujer",
                    "weight": 75.0,
                    "height": 160.0,
                    "clinical": {
                        "total_cholesterol": 200.0,
                        "hdl": 40.0,
                        "ldl": 130.0,
                        "systolic_pressure": 150,
                        "diastolic_pressure": 85
                    },
                    "risk_factors": {
                        "smoking": False,
                        "diabetes": True,
                        "hypertension_treatment": True,
                        "statins": True
                    }
                }
            ]
        },
        {
            "name": "adulto_riesgo_alto",
            "description": "Perfil de adulto con riesgo alto",
            "patients": [
                {
                    "name": "Adulto Riesgo Alto",
                    "age": 70,
                    "sex": "hombre",
                    "weight": 90.0,
                    "height": 175.0,
                    "clinical": {
                        "total_cholesterol": 250.0,
                        "hdl": 35.0,
                        "ldl": 180.0,
                        "systolic_pressure": 160,
                        "diastolic_pressure": 95
                    },
                    "risk_factors": {
                        "smoking": True,
                        "diabetes": True,
                        "hypertension_treatment": True,
                        "statins": True
                    }
                }
            ]
        }
    ]
    
    db = get_session()
    try:
        # Verificar si ya existen perfiles
        existing_profiles = db.query(Profile).count()
        if existing_profiles > 0:
            print("Los perfiles ya existen en la base de datos.")
            return
        
        # Crear perfiles y pacientes
        for profile_data in profiles_data:
            profile = Profile(
                name=profile_data["name"],
                description=profile_data["description"]
            )
            db.add(profile)
            db.flush()  # Para obtener el ID del perfil
            
            for patient_data in profile_data["patients"]:
                patient = Patient(
                    profile_id=profile.id,
                    name=patient_data["name"],
                    age=patient_data["age"],
                    sex=patient_data["sex"],
                    weight=patient_data["weight"],
                    height=patient_data["height"]
                )
                db.add(patient)
                db.flush()  # Para obtener el ID del paciente
                
                # Crear medición clínica
                clinical = ClinicalMeasurement(
                    patient_id=patient.id,
                    measurement_date=datetime.utcnow(),
                    total_cholesterol=patient_data["clinical"]["total_cholesterol"],
                    hdl=patient_data["clinical"]["hdl"],
                    ldl=patient_data["clinical"]["ldl"],
                    systolic_pressure=patient_data["clinical"]["systolic_pressure"],
                    diastolic_pressure=patient_data["clinical"]["diastolic_pressure"]
                )
                db.add(clinical)
                
                # Crear factores de riesgo
                risk_factors = RiskFactorsHistory(
                    patient_id=patient.id,
                    date_recorded=datetime.utcnow(),
                    smoking=patient_data["risk_factors"]["smoking"],
                    diabetes=patient_data["risk_factors"]["diabetes"],
                    hypertension_treatment=patient_data["risk_factors"]["hypertension_treatment"],
                    statins=patient_data["risk_factors"]["statins"]
                )
                db.add(risk_factors)
        
        db.commit()
        print("✅ Perfiles creados correctamente")
        print(f"📈 Total de perfiles creados: {len(profiles_data)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creando perfiles: {e}")
        print(f"🔍 Detalles del error: {type(e).__name__}: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
