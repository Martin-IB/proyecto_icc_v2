const API_URL = "http://localhost:8000/biorreactor";

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    const form = document.getElementById("biorreactorForm");
    const codigoInput = document.getElementById("nombre");
    const ubicacionInput = document.getElementById("ubicacion");
    const idInput = document.getElementById("biorreactorId");
    const tableBody = document.getElementById("biorreactorTableBody");

    if (!form || !codigoInput || !ubicacionInput || !idInput || !tableBody) {
      console.warn("⚠️ Elementos del módulo biorreactor aún no disponibles.");
      return;
    }

    cargarBiorreactores();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        codigo: parseInt(codigoInput.value),
        ubicacion: ubicacionInput.value,
        estado: "activo"
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

      biorreactores.forEach(b => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${b.id}</td>
          <td>${b.codigo}</td>
          <td>${b.ubicacion || ''}</td>
          <td>
            <button class="btn btn-warning btn-sm" onclick="editarBiorreactor(${b.id}, ${b.codigo}, '${b.ubicacion}')">Editar</button>
            <button class="btn btn-danger btn-sm" onclick="eliminarBiorreactor(${b.id})">Eliminar</button>
          </td>
        `;

        tableBody.appendChild(row);
      });
    }

    window.editarBiorreactor = function (id, codigo, ubicacion) {
      idInput.value = id;
      codigoInput.value = codigo;
      ubicacionInput.value = ubicacion;
    };

    window.eliminarBiorreactor = async function (id) {
      if (confirm("¿Deseas eliminar este biorreactor?")) {
        await fetch(`${API_URL}/${id}`, {
          method: "DELETE"
        });
        cargarBiorreactores();
      }
    };
  }, 100);
});
