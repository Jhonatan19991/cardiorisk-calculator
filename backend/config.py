"""
Configuración de la aplicación
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Configuración de base de datos
DATABASE_URL = os.getenv('DATABASE_URL', '1')

# Configuración de la aplicación
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Configuración de sesiones
EXPIRE_MINUTES = int(os.getenv('EXPIRE_MINUTES', 60))
