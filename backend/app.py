"""
Servidor Flask principal para la Calculadora de Riesgo Cardiovascular
Autor: <tu-nombre>
Licencia: MIT
"""

from datetime import datetime, timedelta
from uuid import uuid4

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from calculators import (
    framingham_risk,
    score_risk,
    acc_aha_risk,
    get_default_profile,
    get_all_profiles,
)
from validators import validate_patient_data
from report_generator import build_pdf_report
from models import create_tables, get_session, Profile, Patient, ClinicalMeasurement, RiskFactorsHistory
from datetime import datetime
from config import EXPIRE_MINUTES

# In-memory store con expiración configurable
SESSIONS = {}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar base de datos
create_tables()


def _cleanup_expired():
    """Elimina resultados almacenados con más de EXPIRE_MINUTES."""
    now = datetime.utcnow()
    expired = [
        sid for sid, data in SESSIONS.items()
        if now - data["timestamp"] > timedelta(minutes=EXPIRE_MINUTES)
    ]
    for sid in expired:
        del SESSIONS[sid]


@app.route("/profiles", methods=["GET"])
def get_profiles():
    """Obtiene todos los perfiles de pacientes predefinidos."""
    return jsonify({
        "status": "ok",
        "profiles": get_all_profiles()
    })


@app.route("/profiles", methods=["POST"])
def create_profile():
    """Crea un nuevo perfil de paciente."""
    data = request.json or {}
    
    # Validar datos requeridos
    required_fields = ["name", "description", "patient_data"]
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "errors": [f"Campo requerido: {field}"]}), 400
    
    patient_data = data["patient_data"]
    
    # Validar datos del paciente
    ok, warnings_or_errors = validate_patient_data(patient_data)
    if not ok:
        return jsonify({"status": "error", "errors": warnings_or_errors}), 400
    
    db = get_session()
    try:
        # Verificar si el perfil ya existe
        existing_profile = db.query(Profile).filter(Profile.name == data["name"]).first()
        if existing_profile:
            return jsonify({"status": "error", "errors": ["Ya existe un perfil con ese nombre"]}), 400
        
        # Crear perfil
        profile = Profile(
            name=data["name"],
            description=data["description"]
        )
        db.add(profile)
        db.flush()  # Para obtener el ID
        
        # Crear paciente
        patient = Patient(
            profile_id=profile.id,
            name=patient_data.get("nombre", data["name"]),
            age=patient_data["edad"],
            sex=patient_data["sexo"],
            weight=patient_data.get("peso", 0),
            height=patient_data.get("altura", 0)
        )
        db.add(patient)
        db.flush()  # Para obtener el ID
        
        # Crear medición clínica
        clinical = ClinicalMeasurement(
            patient_id=patient.id,
            measurement_date=datetime.utcnow(),
            total_cholesterol=patient_data["colesterol_total"],
            hdl=patient_data["hdl"],
            ldl=patient_data.get("ldl", 0),
            systolic_pressure=patient_data["presion_sistolica"],
            diastolic_pressure=patient_data.get("presion_diastolica", 0)
        )
        db.add(clinical)
        
        # Crear factores de riesgo
        risk_factors = RiskFactorsHistory(
            patient_id=patient.id,
            date_recorded=datetime.utcnow(),
            smoking=patient_data.get("fumador", False),
            diabetes=patient_data.get("diabetes", False),
            hypertension_treatment=patient_data.get("tratamiento_hipertension", False),
            statins=patient_data.get("estatinas", False)
        )
        db.add(risk_factors)
        
        db.commit()
        
        return jsonify({
            "status": "ok",
            "message": "Perfil creado exitosamente",
            "profile_id": profile.id
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "errors": [f"Error creando perfil: {str(e)}"]}), 500
    finally:
        db.close()


@app.route("/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    """Elimina un perfil."""
    db = get_session()
    try:
        profile = db.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return jsonify({"status": "error", "errors": ["Perfil no encontrado"]}), 404
        
        db.delete(profile)
        db.commit()
        
        return jsonify({
            "status": "ok",
            "message": "Perfil eliminado exitosamente"
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "errors": [f"Error eliminando perfil: {str(e)}"]}), 500
    finally:
        db.close()


@app.route("/profiles/<string:profile_name>/history", methods=["GET"])
def get_profile_history(profile_name):
    """Obtiene el historial de mediciones de un perfil."""
    db = get_session()
    try:
        profile = db.query(Profile).filter(Profile.name == profile_name, Profile.is_active == True).first()
        if not profile:
            return jsonify({"status": "error", "errors": ["Perfil no encontrado"]}), 404
        
        # Obtener el primer paciente del perfil
        patient = db.query(Patient).filter(Patient.profile_id == profile.id).first()
        if not patient:
            return jsonify({"status": "error", "errors": ["Paciente no encontrado"]}), 404
        
        # Obtener historial de mediciones clínicas
        clinical_history = db.query(ClinicalMeasurement).filter(
            ClinicalMeasurement.patient_id == patient.id
        ).order_by(ClinicalMeasurement.measurement_date.desc()).all()
        
        # Obtener historial de factores de riesgo
        risk_factors_history = db.query(RiskFactorsHistory).filter(
            RiskFactorsHistory.patient_id == patient.id
        ).order_by(RiskFactorsHistory.date_recorded.desc()).all()
        
        # Combinar historiales por fecha
        history = []
        for clinical in clinical_history:
            # Buscar factores de riesgo de la misma fecha o más recientes
            risk_factors = next(
                (rf for rf in risk_factors_history 
                 if rf.date_recorded.date() <= clinical.measurement_date.date()), 
                None
            )
            
            history.append({
                "date": clinical.measurement_date.isoformat(),
                "clinical": {
                    "total_cholesterol": float(clinical.total_cholesterol) if clinical.total_cholesterol else None,
                    "hdl": float(clinical.hdl) if clinical.hdl else None,
                    "ldl": float(clinical.ldl) if clinical.ldl else None,
                    "systolic_pressure": clinical.systolic_pressure,
                    "diastolic_pressure": clinical.diastolic_pressure
                },
                "risk_factors": {
                    "smoking": risk_factors.smoking if risk_factors else False,
                    "diabetes": risk_factors.diabetes if risk_factors else False,
                    "hypertension_treatment": risk_factors.hypertension_treatment if risk_factors else False,
                    "statins": risk_factors.statins if risk_factors else False
                } if risk_factors else None
            })
        
        return jsonify({
            "status": "ok",
            "profile_name": profile.name,
            "patient_name": patient.name,
            "current_data": {
                "age": patient.age,
                "weight": float(patient.weight) if patient.weight else None,
                "height": float(patient.height) if patient.height else None
            },
            "history": history
        })
        
    except Exception as e:
        return jsonify({"status": "error", "errors": [f"Error obteniendo historial: {str(e)}"]}), 500
    finally:
        db.close()


@app.route("/profiles/<string:profile_name>/update", methods=["POST"])
def update_profile_measurements(profile_name):
    """Actualiza las mediciones de un perfil existente."""
    data = request.json or {}
    
    # Validar datos del paciente
    ok, warnings_or_errors = validate_patient_data(data)
    if not ok:
        return jsonify({"status": "error", "errors": warnings_or_errors}), 400
    
    db = get_session()
    try:
        profile = db.query(Profile).filter(Profile.name == profile_name, Profile.is_active == True).first()
        if not profile:
            return jsonify({"status": "error", "errors": ["Perfil no encontrado"]}), 404
        
        # Obtener el primer paciente del perfil
        patient = db.query(Patient).filter(Patient.profile_id == profile.id).first()
        if not patient:
            return jsonify({"status": "error", "errors": ["Paciente no encontrado"]}), 404
        
        # Actualizar datos personales del paciente
        patient.age = data.get("edad", patient.age)
        patient.weight = data.get("peso", patient.weight)
        patient.height = data.get("altura", patient.height)
        patient.updated_at = datetime.utcnow()
        
        # Crear nueva medición clínica
        clinical = ClinicalMeasurement(
            patient_id=patient.id,
            measurement_date=datetime.utcnow(),
            total_cholesterol=data["colesterol_total"],
            hdl=data["hdl"],
            ldl=data.get("ldl", 0),
            systolic_pressure=data["presion_sistolica"],
            diastolic_pressure=data.get("presion_diastolica", 0)
        )
        db.add(clinical)
        
        # Crear nuevos factores de riesgo
        risk_factors = RiskFactorsHistory(
            patient_id=patient.id,
            date_recorded=datetime.utcnow(),
            smoking=data.get("fumador", False),
            diabetes=data.get("diabetes", False),
            hypertension_treatment=data.get("tratamiento_hipertension", False),
            statins=data.get("estatinas", False)
        )
        db.add(risk_factors)
        
        db.commit()
        
        return jsonify({
            "status": "ok",
            "message": "Mediciones actualizadas exitosamente"
        })
        
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "errors": [f"Error actualizando mediciones: {str(e)}"]}), 500
    finally:
        db.close()


@app.route("/profiles/<string:profile_name>", methods=["GET"])
def get_profile(profile_name):
    """Obtiene un perfil específico por nombre."""
    profile = get_default_profile(profile_name)
    if not profile:
        return jsonify({"status": "error", "errors": ["Perfil no encontrado"]}), 404
    
    return jsonify({
        "status": "ok",
        "profile": profile
    })


@app.route("/calculate/<string:method>", methods=["POST"])
def calculate(method):
    """
    Calcula riesgo según el método indicado:
    framingham | score | acc-aha | all
    """
    _cleanup_expired()
    patient = request.json or {}

    # Validación de datos de entrada
    ok, warnings_or_errors = validate_patient_data(patient)
    if not ok:
        return jsonify({"status": "error", "errors": warnings_or_errors}), 400

    result = {}
    try:
        if method in ("framingham", "all"):
            result["framingham"] = framingham_risk(patient)
        if method in ("score", "all"):
            result["score"] = score_risk(patient)
        if method in ("acc-aha", "all"):
            result["acc_aha"] = acc_aha_risk(patient)
    except Exception as err:
        # Capturar cualquier error durante el cálculo
        return jsonify({"status": "error", "errors": [f"Error en cálculo: {str(err)}"]}), 422

    # Verificar que no haya errores en los resultados
    for method_name, method_result in result.items():
        if "error" in method_result:
            return jsonify({"status": "error", "errors": [f"Error en {method_name}: {method_result['error']}"]}), 422

    # Almacenar sesión temporal
    session_id = str(uuid4())
    SESSIONS[session_id] = {
        "timestamp": datetime.utcnow(),
        "patient": patient,
        "result": result,
        "warnings": warnings_or_errors,
    }
    return jsonify({
        "status": "ok",
        "session_id": session_id,
        "result": result,
        "warnings": warnings_or_errors,
    })


@app.route("/generate-report/<string:session_id>", methods=["GET"])
def generate_report(session_id):
    """Genera un PDF profesional con los resultados almacenados."""
    _cleanup_expired()
    data = SESSIONS.get(session_id)
    if not data:
        return jsonify({"status": "error", "errors": ["Sesión no encontrada"]}), 404

    try:
        pdf_path = build_pdf_report(
            patient=data["patient"],
            result=data["result"],
            warnings=data["warnings"],
        )
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": "error", "errors": [f"Error generando PDF: {str(e)}"]}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificación de salud del servidor."""
    return jsonify({"status": "ok", "message": "Servidor funcionando correctamente"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
