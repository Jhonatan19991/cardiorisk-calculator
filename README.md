# Calculadora de Riesgo Cardiovascular

Este repositorio contiene el desarrollo de una aplicación web integral para la estimación del riesgo cardiovascular, diseñada con fines académicos y clínicos. La herramienta permite calcular dicho riesgo mediante la implementación de escalas reconocidas internacionalmente, como Framingham, SCORE 2019 y ACC/AHA, integrando criterios médicos y parámetros fisiológicos del paciente.


## 📑 Tabla de Contenidos  

1. [Características](#características)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Uso](#uso)
4. [Escalas de Riesgo](#escalas-de-riesgo)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [API Endpoints](#api-endpoints)
7. [Base de Datos](#base-de-datos)
8. [Credenciales de Conexión](#credenciales-de-conexión)
9. [Notas Médicas](#notas-médicas)
10. [Solución de Problemas](#solución-de-problemas)


## Características

- **Cálculos científicos precisos** basados en la literatura médica actual
- **Múltiples escalas de riesgo**: Framingham 2008, SCORE 2019, ACC/AHA 2013
- **Perfiles de pacientes predefinidos** para facilitar las pruebas
- **Validación robusta** de datos clínicos
- **Generación de reportes PDF** profesionales
- **Interfaz moderna y responsiva** con gráficos interactivos

## Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Backend

1. Navega al directorio del backend:
   ```bash
   cd backend
   ```

2. Crea el archivo `.env` copiando el ejemplo (cambia el DATABASE_URL):
   ```bash
   copy env.example .env
   ```
   > En macOS/Linux usa:
   > ```bash
   > cp env.example .env
   > ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta el servidor:
   ```bash
   python app.py
   ```

El backend estará disponible en `http://localhost:5000`

### Frontend

1. Abre el archivo `frontend/index.html` en tu navegador web
2. O ejecuta un servidor local simple:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
   Luego abre `http://localhost:8000` en tu navegador

## Uso

### Perfiles Predefinidos

La aplicación incluye 4 perfiles de pacientes predefinidos:

1. **Joven Sano** - Paciente de bajo riesgo
2. **Adulto Riesgo Moderado** - Paciente con factores de riesgo moderados
3. **Adulta Diabética** - Paciente con diabetes y riesgo elevado
4. **Adulto Riesgo Alto** - Paciente con múltiples factores de alto riesgo

Haz clic en cualquier perfil para cargar automáticamente los datos en el formulario.

### Cálculo Manual

1. Completa el formulario con los datos del paciente
2. Haz clic en "Calcular Riesgo"
3. Revisa los resultados y gráficos
4. Genera un reporte PDF si es necesario

## Escalas de Riesgo

### Framingham 2008
- Basada en el estudio Framingham Heart Study
- Considera edad, sexo, colesterol total, HDL, presión sistólica, diabetes y tabaquismo
- Aplicable a pacientes de 30 a 74 años

### SCORE 2019
- Sistema de puntuación europeo actualizado
- Adaptado para regiones de alto riesgo cardiovascular
- Incluye factores de riesgo tradicionales más precisos
- Aplicable a pacientes de 40 a 65 años

### ACC/AHA 2013
- Guías americanas de cardiología
- Ecuaciones de cohorte agrupadas
- Considera tratamiento antihipertensivo y estatinas
- Aplicable a pacientes de 40 a 79 años

## Estructura del Proyecto

```
cardiorisk_vFAIL/
├── backend/
│   ├── app.py              # Servidor Flask principal
│   ├── calculators.py      # Algoritmos de cálculo de riesgo
│   ├── validators.py       # Validación de datos clínicos
│   ├── report_generator.py # Generación de reportes PDF
│   ├── requirements.txt    # Dependencias de Python
│   └── reports/            # Directorio de reportes generados
├── frontend/
│   ├── index.html          # Página principal
│   ├── script.js           # Lógica de la aplicación
│   ├── styles.css          # Estilos CSS
│   └── assets/
│       └── charts.js       # Generación de gráficos
└── README.md               # Este archivo
```

## API Endpoints

- `GET /profiles` - Obtiene todos los perfiles predefinidos
- `GET /profiles/<nombre>` - Obtiene un perfil específico
- `POST /calculate/<método>` - Calcula riesgo (framingham, score, acc-aha, all)
- `GET /generate-report/<session_id>` - Genera reporte PDF
- `GET /health` - Verificación de salud del servidor

## Base de datos

## Diagrama de relaciones
![Diagrama de bloques](https://github.com/Jhonatan19991/cardiorisk-calculator/blob/dev/diag_base.png)

### Descripción de la base de datos

### 1. **profiles** 
Contiene información de los perfiles que clasifican a los pacientes (ejemplo: perfil poblacional, grupo de riesgo, cohortes específicas).  

| Campo        | Tipo        | Descripción |
|--------------|------------|-------------|
| `id`         | SERIAL (PK) | Identificador único del perfil. |
| `name`       | VARCHAR(100) | Nombre del perfil. |
| `description`| TEXT        | Descripción detallada del perfil. |
| `is_active`  | BOOLEAN     | Indica si el perfil está activo. |
| `created_at` | TIMESTAMP   | Fecha de creación. |
| `updated_at` | TIMESTAMP   | Última fecha de actualización. |

---
### 2. **patients**  
Registra la información básica de cada paciente.  

| Campo        | Tipo        | Descripción |
|--------------|------------|-------------|
| `id`         | SERIAL (PK) | Identificador único del paciente. |
| `profile_id` | INT (FK)    | Relación con `profiles.id`. |
| `name`       | VARCHAR(150) | Nombre completo del paciente. |
| `age`        | INT         | Edad del paciente. |
| `sex`        | VARCHAR(10) | Sexo del paciente (`hombre`, `mujer`). |
| `weight`     | DECIMAL(5,2) | Peso en kilogramos. |
| `height`     | DECIMAL(5,2) | Estatura en centímetros. |
| `created_at` | TIMESTAMP   | Fecha de registro. |
| `updated_at` | TIMESTAMP   | Última actualización. |

---

### 3.  **clinical_measurements**  
Guarda los valores clínicos periódicos de los pacientes. Estos datos son esenciales para calcular el riesgo cardiovascular.  

| Campo              | Tipo        | Descripción |
|--------------------|-------------|-------------|
| `id`               | SERIAL (PK) | Identificador único de la medición. |
| `patient_id`       | INT (FK)    | Relación con `patients.id`. |
| `measurement_date` | TIMESTAMP   | Fecha y hora de la medición. |
| `total_cholesterol`| DECIMAL(6,2) | Colesterol total (mg/dL). |
| `hdl`              | DECIMAL(6,2) | Colesterol HDL (mg/dL). |
| `ldl`              | DECIMAL(6,2) | Colesterol LDL (mg/dL). |
| `systolic_pressure`| INT         | Presión arterial sistólica (mmHg). |
| `diastolic_pressure`| INT        | Presión arterial diastólica (mmHg). |
| `created_at`       | TIMESTAMP   | Fecha de registro. |

---

### 4. **risk_factors_history**  
Registra los factores de riesgo clínicos y hábitos que pueden influir en el cálculo de riesgo cardiovascular.  

| Campo                  | Tipo        | Descripción |
|------------------------|-------------|-------------|
| `id`                   | SERIAL (PK) | Identificador único del historial. |
| `patient_id`           | INT (FK)    | Relación con `patients.id`. |
| `date_recorded`        | TIMESTAMP   | Fecha del registro del historial. |
| `smoking`              | BOOLEAN     | Indica si el paciente fuma. |
| `diabetes`             | BOOLEAN     | Indica diagnóstico de diabetes. |
| `hypertension_treatment` | BOOLEAN  | Indica tratamiento para hipertensión. |
| `statins`              | BOOLEAN     | Uso de estatinas. |
| `created_at`           | TIMESTAMP   | Fecha de registro. |

---


### Justificación del Diseño
- La base de datos se encuentra normalizada para evitar la redundacia de datos. Se almacena las entidades  `patients`, `profiles`, en tablas distintas a las de las mediciones concurrentes `clinical_measurements`,  `risk_factors_history` para mayor eficiencia y facilidad en su mantenimiento. 

- Se usa claves primarias y foráneas para establecer relaciones claras y garantizar la integridad referencial. 

- Se añaden los campos  `created_at` y  `updated_at`, para el seguimiento de hora de creación y hora de actualización de los datos, útil para realizar depuraciones o análisis históricos. 

### Credenciales de conexión

- Crea un archivo `.env`  dentro de la carpeta `backend/` con el siguiente contenido:


```env
DATABASE_URL="postgresql://mi_usuario:mi_contraseña@localhost:5432/mi_base_de_datos"
DEBUG=True
HOST=0.0.0.0
PORT=5000
EXPIRE_MINUTES=60
```

---

## Validaciones

La aplicación incluye validaciones robustas para:

- **Rangos clínicos** apropiados para cada parámetro
- **Campos obligatorios** para cálculos precisos
- **Advertencias médicas** para valores límite
- **Validaciones específicas** por edad y factores de riesgo

## Tecnologías Utilizadas

- **Backend**: Python, Flask, NumPy, ReportLab
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Chart.js
- **Cálculos**: Algoritmos científicos validados de la literatura médica

## Notas Médicas

⚠️ **Importante**: Esta calculadora es una herramienta educativa y de apoyo clínico. Los resultados no sustituyen el criterio médico profesional. Siempre consulte con un profesional de la salud para decisiones médicas.

## Solución de Problemas

### Error de conexión al backend
- Verifica que el servidor Flask esté ejecutándose
- Confirma que el puerto 5000 esté disponible
- Revisa la consola del navegador para errores de CORS

### Errores de cálculo
- Verifica que todos los campos obligatorios estén completos
- Confirma que los valores estén dentro de los rangos permitidos
- Revisa los logs del servidor para errores específicos

### Problemas con reportes PDF
- Asegúrate de que el directorio `backend/reports/` tenga permisos de escritura
- Verifica que ReportLab esté instalado correctamente

## Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa los cambios
4. Añade tests si es posible
5. Envía un pull request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Contacto

Para preguntas o soporte técnico, por favor abre un issue en el repositorio.