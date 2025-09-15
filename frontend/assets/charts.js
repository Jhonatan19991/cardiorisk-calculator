/* Generación de gráficos con Chart.js */
function generateCharts(result){
  const container = document.getElementById("charts");
  container.innerHTML = `<canvas id="barChart"></canvas>`;
  const ctx = document.getElementById("barChart").getContext("2d");
  
  // Construir datos solo para métodos disponibles
  const labels = [];
  const data = [];
  const backgroundColor = [];
  
  if (result.framingham) {
    labels.push("Framingham");
    data.push(result.framingham.percent);
    backgroundColor.push("#2E7D32");
  }
  
  if (result.score) {
    labels.push("SCORE 2019");
    data.push(result.score.percent);
    backgroundColor.push("#F9A825");
  }
  
  if (result.acc_aha) {
    labels.push("ACC/AHA");
    data.push(result.acc_aha.percent);
    backgroundColor.push("#C62828");
  }
  
  // Solo crear el gráfico si hay datos disponibles
  if (labels.length > 0) {
    const chartData = {
      labels: labels,
      datasets:[{
        label:"Riesgo (%)",
        data: data,
        backgroundColor: backgroundColor
      }]
    };
    new Chart(ctx,{type:"bar",data: chartData});
  } else {
    container.innerHTML = "<p>No hay datos disponibles para generar gráficos.</p>";
  }
}
