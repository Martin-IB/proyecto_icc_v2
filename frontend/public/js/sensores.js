(() => {
  const API_URL = "http://18.188.154.229:8000/sensores";
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const esAdmin = usuario?.Tipo_idTipo === 1 || usuario?.Tipo_idTipo === 2;

  async function cargarSensores() {
    const tbody = document.getElementById("sensorTableBody");
    const formAdmin = document.getElementById("formularioAdminSensor");

    if (esAdmin && formAdmin) formAdmin.style.display = "block";

    const res = await fetch(API_URL);
    const sensores = await res.json();
    tbody.innerHTML = "";

    sensores.forEach(s => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${s.tipo}</td>
        <td>${s.modelo}</td>
        <td>${s.ubicacion}</td>
        <td>${s.Biorreactor_idBiorreactor}</td>
        ${
          esAdmin
            ? `<td>
                <button class="btn btn-warning btn-sm" onclick="editarSensor(${s.idSensores}, '${s.tipo}', '${s.modelo}', '${s.ubicacion}', ${s.Biorreactor_idBiorreactor})">Editar</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarSensor(${s.idSensores})">Eliminar</button>
              </td>`
            : ""
        }
      `;
      tbody.appendChild(row);
    });
  }

  document.getElementById("sensorForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      tipo: document.getElementById("tipo").value,
      modelo: document.getElementById("modelo").value,
      ubicacion: document.getElementById("ubicacion").value,
      Biorreactor_idBiorreactor: parseInt(document.getElementById("biorreactor").value)
    };

    const id = document.getElementById("sensorId").value;
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/${id}` : API_URL;

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    document.getElementById("sensorForm").reset();
    document.getElementById("sensorId").value = "";
    cargarSensores();
  });

  window.editarSensor = (id, tipo, modelo, ubicacion, bior) => {
    document.getElementById("sensorId").value = id;
    document.getElementById("tipo").value = tipo;
    document.getElementById("modelo").value = modelo;
    document.getElementById("ubicacion").value = ubicacion;
    document.getElementById("biorreactor").value = bior;
  };

  window.eliminarSensor = async (id) => {
    if (!confirm("¿Eliminar sensor?")) return;
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarSensores();
  };

  cargarSensores();
})();
