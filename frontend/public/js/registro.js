(() => {
  const API_URL = "http://3.132.200.37:8000/registro";
  //const API_URL = "http://localhost:8000/registro";
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const esAdmin = usuario?.Tipo_idTipo === 1 || usuario?.Tipo_idTipo === 2;

  async function cargarRegistros() {
    const tbody = document.getElementById("registroTableBody");
    const formAdmin = document.getElementById("formularioAdminRegistro");

    if (esAdmin && formAdmin) formAdmin.style.display = "block";

    const res = await fetch(API_URL);
    const registros = await res.json();
    tbody.innerHTML = "";

    registros.forEach(r => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${r.tipo_evento}</td>
        <td>${r.description}</td>
        <td>${new Date(r.fecha).toLocaleString()}</td>
        <td>${r.Biorreactor_idBiorreactor}</td>
        <td>${r.Sensores_idSensores}</td>
        ${
          esAdmin
            ? `<td>
                <button class="btn btn-warning btn-sm" onclick="editarRegistro(${r.idRegistro}, '${r.tipo_evento}', '${r.description}', ${r.Biorreactor_idBiorreactor}, ${r.Sensores_idSensores})">Editar</button>
                <button class="btn btn-danger btn-sm" onclick="eliminarRegistro(${r.idRegistro})">Eliminar</button>
              </td>`
            : ""
        }
      `;
      tbody.appendChild(row);
    });
  }

  document.getElementById("registroForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      tipo_evento: document.getElementById("tipo_evento").value,
      description: document.getElementById("descripcion").value,
      Usuario_idUsuario: usuario?.idUsuario,
      Biorreactor_idBiorreactor: parseInt(document.getElementById("biorreactor").value),
      Sensores_idSensores: parseInt(document.getElementById("sensor").value)
    };

    const id = document.getElementById("registroId").value;
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/${id}` : API_URL;

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    document.getElementById("registroForm").reset();
    document.getElementById("registroId").value = "";
    cargarRegistros();
  });

  window.editarRegistro = (id, tipo_evento, description, bior, sensor) => {
    document.getElementById("registroId").value = id;
    document.getElementById("tipo_evento").value = tipo_evento;
    document.getElementById("descripcion").value = description;
    document.getElementById("biorreactor").value = bior;
    document.getElementById("sensor").value = sensor;
  };

  window.eliminarRegistro = async (id) => {
    if (!confirm("¿Eliminar registro?")) return;
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarRegistros();
  };

  cargarRegistros();
})();
