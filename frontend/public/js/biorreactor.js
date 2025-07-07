(() => {
  const API_URL = "http://localhost:8000/biorreactor";
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const esAdmin = usuario?.Tipo_idTipo === 1;

  function iniciarBiorreactor() {
    const form = document.getElementById("biorreactorForm");
    const formularioAdmin = document.getElementById("formularioAdmin");
    const codigoInput = document.getElementById("nombre");
    const ubicacionInput = document.getElementById("ubicacion");
    const idInput = document.getElementById("biorreactorId");
    const tableBody = document.getElementById("biorreactorTableBody");
    const thead = document.getElementById("biorreactorThead");

    if (!form || !codigoInput || !ubicacionInput || !idInput || !tableBody || !thead) {
      console.warn("Esperando a que el DOM esté listo para biorreactores...");
      setTimeout(iniciarBiorreactor, 100);
      return;
    }

    // Mostrar formulario solo si es admin
    if (esAdmin && formularioAdmin) {
      formularioAdmin.style.display = "block";
    }

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        codigo: parseInt(codigoInput.value),
        ubicacion: ubicacionInput.value,
        estado: "activo",
        Usuario_idUsuario: usuario.idUsuario 
      };

      const id = idInput.value;

      if (id) {
        await fetch(`${API_URL}/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
      } else {
        await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });
      }

      form.reset();
      idInput.value = "";
      cargarBiorreactores();
    });

    async function cargarBiorreactores() {
      const res = await fetch(API_URL);
      const biorreactores = await res.json();

      tableBody.innerHTML = "";

      // Encabezados
      thead.innerHTML = `
        <tr>
          <th>Código</th>
          <th>Ubicación</th>
          ${esAdmin ? "<th>Acciones</th>" : ""}
        </tr>
      `;

      biorreactores.forEach(b => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${b.codigo}</td>
          <td>${b.ubicacion || ''}</td>
          ${
            esAdmin
              ? `<td>
                  <button class="btn btn-warning btn-sm" onclick="editarBiorreactor(${b.idBiorreactor}, ${b.codigo}, '${b.ubicacion}')">Editar</button>
                  <button class="btn btn-danger btn-sm" onclick="eliminarBiorreactor(${b.idBiorreactor})">Eliminar</button>
                </td>`
              : ""
          }
        `;

        tableBody.appendChild(row);
      });
    }

    window.editarBiorreactor = function (id, codigo, ubicacion) {
      if (!esAdmin) return;
      idInput.value = id;
      codigoInput.value = codigo;
      ubicacionInput.value = ubicacion;
    };

    window.eliminarBiorreactor = async function (id) {
      if (!esAdmin) return;
      if (confirm("¿Deseas eliminar este biorreactor?")) {
        await fetch(`${API_URL}/${id}`, {
          method: "DELETE"
        });
        cargarBiorreactores();
      }
    };

    // Cargar al iniciar
    cargarBiorreactores();
  }

  iniciarBiorreactor();
})();
