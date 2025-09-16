/* Lógica principal en JavaScript ES6+ */
const API_URL = "http://localhost:5000";
const form = document.getElementById("risk-form");
const resultsSection = document.getElementById("results");
const chartsDiv = document.getElementById("charts");
const interpretationDiv = document.getElementById("interpretation");
const btnPdf = document.getElementById("btn-pdf");
const profileSelect = document.getElementById("profile-select");
const loadProfileBtn = document.getElementById("load-profile-btn");
const createProfileBtn = document.getElementById("create-profile-btn");
const createProfileModal = document.getElementById("create-profile-modal");
const createProfileForm = document.getElementById("create-profile-form");
const viewHistoryBtn = document.getElementById("view-history-btn");
const historyModal = document.getElementById("history-modal");
const historyContent = document.getElementById("history-content");
let currentSessionId = null;
let profilesData = {};
let currentProfileName = null;

// Cargar perfiles al iniciar
document.addEventListener("DOMContentLoaded", () => {
  loadProfiles();
  setupEventListeners();
});

function setupEventListeners() {
  // Selector de perfiles
  profileSelect.addEventListener("change", () => {
    const hasSelection = !!profileSelect.value;
    loadProfileBtn.disabled = !hasSelection;
    viewHistoryBtn.disabled = !hasSelection;
    currentProfileName = hasSelection ? profileSelect.value : null;
  });
  
  // Botón cargar perfil
  loadProfileBtn.addEventListener("click", () => {
    if (profileSelect.value) {
      loadProfile(profileSelect.value);
    }
  });
  
  // Botón crear perfil
  createProfileBtn.addEventListener("click", () => {
    createProfileModal.classList.remove("hidden");
  });
  
  // Cerrar modal
  document.querySelector(".close").addEventListener("click", () => {
    createProfileModal.classList.add("hidden");
  });
  
  document.getElementById("cancel-create").addEventListener("click", () => {
    createProfileModal.classList.add("hidden");
  });
  
  // Formulario crear perfil
  createProfileForm.addEventListener("submit", handleCreateProfile);
  
  // Cerrar modal al hacer clic fuera
  createProfileModal.addEventListener("click", (e) => {
    if (e.target === createProfileModal) {
      createProfileModal.classList.add("hidden");
    }
  });
  
  // Botón ver historial
  viewHistoryBtn.addEventListener("click", () => {
    if (currentProfileName) {
      loadProfileHistory(currentProfileName);
    }
  });
  
  // Cerrar modal de historial
  document.getElementById("close-history").addEventListener("click", () => {
    historyModal.classList.add("hidden");
  });
  
  // Cerrar modal de historial al hacer clic fuera
  historyModal.addEventListener("click", (e) => {
    if (e.target === historyModal) {
      historyModal.classList.add("hidden");
    }
  });
}

async function loadProfiles() {
  try {
    const response = await fetch(`${API_URL}/profiles`);
    const data = await response.json();
    
    if (data.status === "ok") {
      profilesData = data.profiles;
      populateProfileSelect(data.profiles);
    } else {
      console.error("Error cargando perfiles:", data.errors);
    }
  } catch (error) {
    console.error("Error cargando perfiles:", error);
  }
}

function populateProfileSelect(profiles) {
  profileSelect.innerHTML = '<option value="">Seleccionar perfil...</option>';
  
  Object.entries(profiles).forEach(([key, profile]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = `${profile.nombre} (${profile.edad} años, ${profile.sexo})`;
    profileSelect.appendChild(option);
  });
}

function getEstimatedRisk(profile) {
  // Estimación simple basada en factores de riesgo
  let risk = 0;
  if (profile.edad > 65) risk += 2;
  if (profile.fumador) risk += 2;
  if (profile.diabetes) risk += 3;
  if (profile.presion_sistolica > 140) risk += 1;
  if (profile.colesterol_total > 200) risk += 1;
  if (profile.hdl < 40) risk += 1;
  
  if (risk <= 2) return "Bajo";
  if (risk <= 4) return "Moderado";
  if (risk <= 6) return "Alto";
  return "Muy alto";
}

function loadProfile(profileKey) {
  if (profilesData[profileKey]) {
    fillFormWithProfile(profilesData[profileKey]);
    form.scrollIntoView({ behavior: "smooth" });
  } else {
    console.error("Perfil no encontrado:", profileKey);
    alert("Error cargando el perfil seleccionado");
  }
}

async function loadProfileHistory(profileName) {
  try {
    historyContent.innerHTML = "<p>Cargando historial...</p>";
    historyModal.classList.remove("hidden");
    
    const response = await fetch(`${API_URL}/profiles/${profileName}/history`);
    const data = await response.json();
    
    if (data.status === "ok") {
      displayHistory(data);
    } else {
      historyContent.innerHTML = `<p>Error cargando historial: ${data.errors.join(", ")}</p>`;
    }
  } catch (error) {
    console.error("Error cargando historial:", error);
    historyContent.innerHTML = "<p>Error cargando el historial</p>";
  }
}

function displayHistory(data) {
  const { profile_name, patient_name, current_data, history } = data;
  
  if (history.length === 0) {
    historyContent.innerHTML = `
      <div class="no-history">
        <h4>No hay mediciones registradas</h4>
        <p>Este perfil aún no tiene mediciones guardadas.</p>
      </div>
    `;
    return;
  }
  
  let html = `
    <h4>Historial de ${patient_name}</h4>
    <div class="current-data">
      <h5>Datos Personales Actuales:</h5>
      <p><strong>Edad:</strong> ${current_data.age || 'N/A'} años</p>
      <p><strong>Peso:</strong> ${current_data.weight || 'N/A'} kg</p>
      <p><strong>Altura:</strong> ${current_data.height || 'N/A'} cm</p>
    </div>
    <table class="history-table">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Colesterol Total</th>
          <th>HDL</th>
          <th>LDL</th>
          <th>Presión Sistólica</th>
          <th>Presión Diastólica</th>
          <th>Factores de Riesgo</th>
        </tr>
      </thead>
      <tbody>
  `;
  
  history.forEach(entry => {
    const date = new Date(entry.date).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
    
    const clinical = entry.clinical;
    const riskFactors = entry.risk_factors;
    
    let riskFactorsText = "N/A";
    if (riskFactors) {
      const factors = [];
      if (riskFactors.smoking) factors.push("Fumador");
      if (riskFactors.diabetes) factors.push("Diabetes");
      if (riskFactors.hypertension_treatment) factors.push("Trat. Hipertensión");
      if (riskFactors.statins) factors.push("Estatinas");
      riskFactorsText = factors.length > 0 ? factors.join(", ") : "Ninguno";
    }
    
    html += `
      <tr>
        <td class="history-date">${date}</td>
        <td class="history-values">${clinical.total_cholesterol || 'N/A'}</td>
        <td class="history-values">${clinical.hdl || 'N/A'}</td>
        <td class="history-values">${clinical.ldl || 'N/A'}</td>
        <td class="history-values">${clinical.systolic_pressure || 'N/A'}</td>
        <td class="history-values">${clinical.diastolic_pressure || 'N/A'}</td>
        <td>${riskFactorsText}</td>
      </tr>
    `;
  });
  
  html += `
      </tbody>
    </table>
  `;
  
  historyContent.innerHTML = html;
}

async function updateProfileMeasurements(profileName, data) {
  try {
    const response = await fetch(`${API_URL}/profiles/${profileName}/update`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
    
    const result = await response.json();
    
    if (result.status === "ok") {
      console.log("Mediciones actualizadas para el perfil:", profileName);
    } else {
      console.warn("Error actualizando mediciones:", result.errors);
    }
  } catch (error) {
    console.error("Error actualizando mediciones del perfil:", error);
  }
}

async function handleCreateProfile(e) {
  e.preventDefault();
  
  const formData = new FormData(createProfileForm);
  const profileName = formData.get("profile_name");
  const profileDescription = formData.get("profile_description");
  const patientName = formData.get("patient_name");
  
  // Obtener datos del formulario principal
  const patientData = Object.fromEntries(new FormData(form).entries());
  
  // Convertir checkboxes a booleanos
  ["fumador", "diabetes", "tratamiento_hipertension", "estatinas"].forEach(
    k => patientData[k] = form.elements[k].checked
  );
  
  // Convertir valores numéricos
  ["edad", "peso", "altura", "colesterol_total", "hdl", "ldl", "presion_sistolica", "presion_diastolica"].forEach(
    k => {
      if (patientData[k] && patientData[k] !== "") {
        patientData[k] = parseFloat(patientData[k]);
      }
    }
  );
  
  // Validar datos requeridos
  const requiredFields = ["edad", "sexo", "colesterol_total", "hdl", "presion_sistolica"];
  const missingFields = requiredFields.filter(field => !patientData[field]);
  
  if (missingFields.length > 0) {
    alert(`Por favor completa los siguientes campos: ${missingFields.join(", ")}`);
    return;
  }
  
  // Agregar nombre del paciente
  patientData.nombre = patientName;
  
  try {
    const response = await fetch(`${API_URL}/profiles`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: profileName,
        description: profileDescription,
        patient_data: patientData
      })
    });
    
    const result = await response.json();
    
    if (result.status === "ok") {
      alert("¡Perfil creado exitosamente!");
      createProfileModal.classList.add("hidden");
      createProfileForm.reset();
      
      // Recargar lista de perfiles
      await loadProfiles();
      
      // Seleccionar el nuevo perfil
      profileSelect.value = profileName;
      currentProfileName = profileName;
      loadProfileBtn.disabled = false;
      viewHistoryBtn.disabled = false;
    } else {
      alert(`Error creando perfil: ${result.errors.join(", ")}`);
    }
  } catch (error) {
    console.error("Error creando perfil:", error);
    alert("Error creando el perfil. Inténtalo de nuevo.");
  }
}

function fillFormWithProfile(profile) {
  // Llenar el formulario con los datos del perfil
  Object.keys(profile).forEach(key => {
    const element = form.elements[key];
    if (element) {
      if (element.type === "checkbox") {
        element.checked = profile[key];
      } else {
        element.value = profile[key];
      }
    }
  });
  
  // Scroll al formulario
  form.scrollIntoView({ behavior: "smooth" });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!validateForm()) return;

  btnPdf.disabled = true;
  interpretationDiv.textContent = "";
  chartsDiv.innerHTML = "";
  // Eliminar advertencias previas para evitar duplicados
  resultsSection.querySelectorAll(".warnings").forEach(el => el.remove());
  resultsSection.classList.add("hidden");

  const data = Object.fromEntries(new FormData(form).entries());

  // Convertir checkboxes a booleanos
  ["fumador", "diabetes", "tratamiento_hipertension", "estatinas"].forEach(
    k => data[k] = form.elements[k].checked
  );

  // Convertir valores numéricos
  ["edad", "peso", "altura", "colesterol_total", "hdl", "ldl", "presion_sistolica", "presion_diastolica"].forEach(
    k => {
      if (data[k] && data[k] !== "") {
        data[k] = parseFloat(data[k]);
      }
    }
  );

  try {
    const res = await fetch(`${API_URL}/calculate/all`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });
    
    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.errors ? errorData.errors.join(", ") : "Error en el servidor");
    }
    
    const json = await res.json();
    if (json.status !== "ok") {
      throw new Error(json.errors ? json.errors.join(", ") : "Error desconocido");
    }

    currentSessionId = json.session_id;
    displayResults(json.result);
    btnPdf.disabled = false;
    
    // Si hay un perfil seleccionado, actualizar mediciones
    if (currentProfileName) {
      await updateProfileMeasurements(currentProfileName, data);
      // Recargar perfiles para mostrar datos actualizados
      await loadProfiles();
      // Mantener la selección actual
      profileSelect.value = currentProfileName;
    }
    
    // Mostrar advertencias si las hay
    if (json.warnings && json.warnings.length > 0) {
      const warningsDiv = document.createElement("div");
      warningsDiv.className = "warnings";
      warningsDiv.innerHTML = "<h3>Advertencias:</h3><ul>" + 
        json.warnings.map(w => `<li>${w}</li>`).join("") + "</ul>";
      resultsSection.appendChild(warningsDiv);
    }
    
  } catch(err) {
    alert("Error: " + err.message);
    console.error("Error details:", err);
  }
});

btnPdf.addEventListener("click", async () => {
  if (!currentSessionId) return;
  
  try {
    const url = `${API_URL}/generate-report/${currentSessionId}`;
    window.open(url, "_blank");
  } catch (error) {
    alert("Error generando el reporte: " + error.message);
  }
});

function validateForm() {
  const requiredFields = ["edad", "sexo", "colesterol_total", "hdl", "presion_sistolica"];
  const errors = [];
  
  requiredFields.forEach(field => {
    const element = form.elements[field];
    if (!element.value || element.value.trim() === "") {
      errors.push(`El campo ${field.replace("_", " ")} es obligatorio`);
    }
  });
  
  // Validaciones específicas
  const edad = parseFloat(form.elements["edad"].value);
  const col = parseFloat(form.elements["colesterol_total"].value);
  const hdl = parseFloat(form.elements["hdl"].value);
  const presion = parseFloat(form.elements["presion_sistolica"].value);
  
  if (edad < 30 || edad > 79) {
    errors.push("Edad debe estar entre 30 y 79 años para al menos una calculadora");
  }
  if (col < 100 || col > 400) {
    errors.push("Colesterol total debe estar entre 100 y 400 mg/dL");
  }
  if (hdl < 20 || hdl > 100) {
    errors.push("HDL debe estar entre 20 y 100 mg/dL");
  }
  if (presion < 90 || presion > 200) {
    errors.push("Presión sistólica debe estar entre 90 y 200 mmHg");
  }
  
  if (errors.length > 0) {
    alert("Errores de validación:\n" + errors.join("\n"));
    return false;
  }
  
  return true;
}

function displayResults(result) {
  resultsSection.classList.remove("hidden");

  // Obtener solo los resultados disponibles
  const availableResults = [];
  if (result.framingham) availableResults.push(result.framingham.percent);
  if (result.score) availableResults.push(result.score.percent);
  if (result.acc_aha) availableResults.push(result.acc_aha.percent);

  // Interpretación textual
  const overall = availableResults.length > 0 ? Math.max(...availableResults) : 0;
  
  let riskCategory = "bajo";
  if (overall >= 20) riskCategory = "muy alto";
  else if (overall >= 10) riskCategory = "alto";
  else if (overall >= 5) riskCategory = "moderado";

  // Construir el desglose solo con métodos disponibles
  let breakdownHtml = "";
  if (result.framingham) {
    breakdownHtml += `<li><strong>Framingham:</strong> ${result.framingham.percent}% (${result.framingham.category})</li>`;
  }
  if (result.score) {
    breakdownHtml += `<li><strong>SCORE 2019:</strong> ${result.score.percent}% (${result.score.category})</li>`;
  }
  if (result.acc_aha) {
    breakdownHtml += `<li><strong>ACC/AHA:</strong> ${result.acc_aha.percent}% (${result.acc_aha.category})</li>`;
  }

  interpretationDiv.innerHTML = `
    <div class="risk-summary">
      <h3>Resumen del Riesgo Cardiovascular</h3>
      <p><strong>Riesgo global estimado:</strong> <span class="risk-${riskCategory.replace(" ", "-")}">${overall}% (${riskCategory})</span></p>
      
      <div class="risk-breakdown">
        <h4>Desglose por método:</h4>
        <ul>
          ${breakdownHtml}
        </ul>
      </div>
    </div>
  `;

  generateCharts(result);
}
