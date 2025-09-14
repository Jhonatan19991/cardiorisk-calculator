# Calculadora de Riesgo Cardiovascular

Una aplicación web completa para calcular el riesgo cardiovascular utilizando múltiples escalas científicas: Framingham, SCORE2 y ACC/AHA.

## Características

- **Cálculos científicos precisos** basados en la literatura médica actual
- **Múltiples escalas de riesgo**: Framingham 2008, SCORE2 2021, ACC/AHA 2013
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
- Aplicable a pacientes de 20-79 años

### SCORE2 2021
- Sistema de puntuación europeo actualizado
- Adaptado para regiones de alto riesgo cardiovascular
- Incluye factores de riesgo tradicionales más precisos

### ACC/AHA 2013
- Guías americanas de cardiología
- Ecuaciones de cohorte agrupadas
- Considera tratamiento antihipertensivo y estatinas

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