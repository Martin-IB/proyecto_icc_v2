(function () {
  const API_URL = "http://18.188.154.229:8000/lectura";
  const tableBody = document.getElementById("lecturaTableBody");
  let chart;

  async function cargarLecturas() {
    const labels = [], tempData = [], humData = [];

    try {
      const res = await fetch(API_URL);
      const lecturas = await res.json();

      tableBody.innerHTML = "";

      lecturas.forEach((l) => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${l.temperatura.toFixed(1)}</td>
          <td>${l.humedad.toFixed(1)}</td>
        `;

        tableBody.appendChild(row);

        // Para el gráfico sí se usa la hora
        labels.push(new Date(l.fecha).toLocaleTimeString());
        tempData.push(l.temperatura);
        humData.push(l.humedad);
      });

    } catch (error) {
      console.error("❌ Error cargando lecturas:", error);
    }

    actualizarGrafico(labels, tempData, humData);
  }

  function actualizarGrafico(labels, temp, hum) {
    const ctx = document.getElementById("graficoSensor").getContext("2d");
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
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

  cargarLecturas();
})();
