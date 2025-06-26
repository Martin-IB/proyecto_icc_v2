const API_URL = "http://localhost:8000/lectura";
const tableBody = document.getElementById("lecturaTableBody");
let chart;

document.addEventListener("DOMContentLoaded", cargarLecturas);

async function cargarLecturas() {


  // Arrays para el gráfico
  const labels = [];
  const tempData = [];
  const humData = [];

  try {
    const res = await fetch(API_URL);
    const lecturas = await res.json();

    tableBody.innerHTML = "";

    lecturas.forEach((l) => {
      const row = document.createElement("tr");
      const fecha = new Date(l.fecha).toLocaleTimeString();
      labels.push(fecha);
      tempData.push(l.temperatura);
      humData.push(l.humedad);

      row.innerHTML = `
        <td>${l.id}</td>
        <td>${l.temperatura.toFixed(1)}</td>
        <td>${l.humedad.toFixed(1)}</td>
        <td>${new Date(l.fecha).toLocaleString()}</td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="eliminar(${l.id})">Eliminar</button>
        </td>
      `;

      tableBody.appendChild(row);
    });

  } catch (error) {
    console.error("Error cargando lecturas:", error);
  }

  actualizarGrafico(labels, tempData, humData);

}

async function eliminar(id) {
  if (confirm("¿Deseas eliminar esta lectura?")) {
    await fetch(`${API_URL}/${id}`, {
      method: "DELETE"
    });
    cargarLecturas();
  }
}



function actualizarGrafico(labels, temp, hum) {
  const ctx = document.getElementById("graficoSensor").getContext("2d");

  if (chart) chart.destroy();  // Evita superposición

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Temperatura (°C)",
          data: temp,
          borderColor: "rgba(255, 99, 132, 1)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          tension: 0.4,
        },
        {
          label: "Humedad (%)",
          data: hum,
          borderColor: "rgba(54, 162, 235, 1)",
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

