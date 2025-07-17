(() => {
  const API_URL = "http://3.132.200.37:8000/empresa";
  //const API_URL = "http://localhost:8000/empresa";
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const esAdmin = usuario?.Tipo_idTipo === 1 || usuario?.Tipo_idTipo === 2;

  async function cargarEmpresas() {
    const tbody = document.getElementById("empresaTableBody");
    const formAdmin = document.getElementById("formularioAdmin");

    if (esAdmin) formAdmin.style.display = "block";

    const res = await fetch(API_URL);
    const empresas = await res.json();
    tbody.innerHTML = "";

    empresas.forEach(e => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${e.nombre}</td><td>${e.ruc}</td><td>${e.correo}</td><td>${e.direccion}</td><td>${e.pais}</td><td>${e.representante}</td><td>${e.telefono}</td>
        <td>
          <button class="btn btn-warning btn-sm" onclick="editarEmpresa(${e.idEmpresa}, '${e.nombre}', '${e.ruc}', '${e.correo}', '${e.direccion}', '${e.pais}', '${e.representante}', '${e.telefono}')">Editar</button>
          <button class="btn btn-danger btn-sm" onclick="eliminarEmpresa(${e.idEmpresa})">Eliminar</button>
        </td>
      `;
      tbody.appendChild(row);
    });
  }

  document.getElementById("empresaForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      nombre: document.getElementById("nombre").value,
      ruc: document.getElementById("ruc").value,
      correo: document.getElementById("correo").value,
      direccion: document.getElementById("direccion").value,
      pais: document.getElementById("pais").value,
      representante: document.getElementById("representante").value,
      telefono: document.getElementById("telefono").value,
      Usuario_idUsuario: usuario?.idUsuario
    };

    const id = document.getElementById("empresaId").value;
    const method = id ? "PUT" : "POST";
    const url = id ? `${API_URL}/${id}` : API_URL;

    await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    document.getElementById("empresaForm").reset();
    document.getElementById("empresaId").value = "";
    cargarEmpresas();
  });

  window.editarEmpresa = (id, nombre, ruc, correo, direccion, pais, representante, telefono) => {
    document.getElementById("empresaId").value = id;
    document.getElementById("nombre").value = nombre;
    document.getElementById("ruc").value = ruc;
    document.getElementById("correo").value = correo;
    document.getElementById("direccion").value = direccion;
    document.getElementById("pais").value = pais;
    document.getElementById("representante").value = representante;
    document.getElementById("telefono").value = telefono;
  };

  window.eliminarEmpresa = async (id) => {
    if (!confirm("¿Eliminar empresa?")) return;
    await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    cargarEmpresas();
  };

  cargarEmpresas();
})();
