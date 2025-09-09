"""
Modelos de base de datos para perfiles de pacientes
Usando SQLAlchemy con PostgreSQL (Supabase)
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Profile(Base):
    """Tabla principal de perfiles de pacientes"""
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    patients = relationship("Patient", back_populates="profile", cascade="all, delete-orphan")

class Patient(Base):
    """Pacientes individuales"""
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    name = Column(String(150), nullable=False)
    age = Column(Integer)
    sex = Column(String(10))  # 'hombre' o 'mujer'
    weight = Column(DECIMAL(5, 2))  # kg
    height = Column(DECIMAL(5, 2))  # cm
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    profile = relationship("Profile", back_populates="patients")
    clinical_measurements = relationship("ClinicalMeasurement", back_populates="patient", cascade="all, delete-orphan")
    risk_factors_history = relationship("RiskFactorsHistory", back_populates="patient", cascade="all, delete-orphan")

class ClinicalMeasurement(Base):
    """Mediciones clínicas del paciente"""
    __tablename__ = 'clinical_measurements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    measurement_date = Column(DateTime, nullable=False)
    total_cholesterol = Column(DECIMAL(6, 2))
    hdl = Column(DECIMAL(6, 2))
    ldl = Column(DECIMAL(6, 2))
    systolic_pressure = Column(Integer)
    diastolic_pressure = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    patient = relationship("Patient", back_populates="clinical_measurements")

class RiskFactorsHistory(Base):
    """Historial de factores de riesgo del paciente"""
    __tablename__ = 'risk_factors_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    date_recorded = Column(DateTime, nullable=False)
    smoking = Column(Boolean, default=False)
    diabetes = Column(Boolean, default=False)
    hypertension_treatment = Column(Boolean, default=False)
    statins = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación
    patient = relationship("Patient", back_populates="risk_factors_history")

# Configuración de base de datos
from config import DATABASE_URL
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Obtiene una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session():
    """Obtiene una sesión de base de datos para uso directo"""
    return SessionLocal()
