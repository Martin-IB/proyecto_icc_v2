
(function () {
  const API_URL_USUARIO = "http://localhost:8000/usuario";

  async function cargarUsuarios() {
    const tableBody = document.getElementById("usuarioTableBody");
    if (!tableBody) {
      console.warn("⚠️ Tabla de usuarios no encontrada.");
      return;
    }

    try {
      const res = await fetch(API_URL_USUARIO);
      const usuarios = await res.json();

      tableBody.innerHTML = "";

      usuarios.forEach((u) => {
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${u.idUsuario}</td>
          <td>${u.nombre}</td>
          <td>${u.email}</td>
          <td>${u.fecha_registro?.split("T")[0] || ""}</td>
          <td>
            <button class="btn btn-warning btn-sm" onclick="editarUsuario(${u.idUsuario}, '${u.nombre}', '${u.email}')">Editar</button>
            <button class="btn btn-danger btn-sm" onclick="eliminarUsuario(${u.idUsuario})">Eliminar</button>
          </td>
        `;

        tableBody.appendChild(row);
      });
    } catch (err) {
      console.error("❌ Error al cargar usuarios:", err);
    }
  }

  window.editarUsuario = function (id, nombre, email) {
    const nombreInput = document.getElementById("nombre");
    const emailInput = document.getElementById("email");
    const idInput = document.getElementById("usuarioId");

    if (!nombreInput || !emailInput || !idInput) return;

    nombreInput.value = nombre;
    emailInput.value = email;
    idInput.value = id;
  };

  window.eliminarUsuario = async function (id) {
    if (confirm("¿Estás seguro de eliminar este usuario?")) {
      await fetch(`${API_URL_USUARIO}/${id}`, {
        method: "DELETE",
      });
      cargarUsuarios();
    }
  };

  setTimeout(() => {
    const form = document.getElementById("usuarioForm");
    if (!form) {
      console.warn("⚠️ Formulario de usuario no encontrado.");
      return;
    }

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const nombre = document.getElementById("nombre")?.value;
      const email = document.getElementById("email")?.value;
      const password = document.getElementById("password")?.value;
      const tipo = 2; // Ajusta según tu lógica
      const id = document.getElementById("usuarioId")?.value;

      if (!nombre || !email || !password) return;

      const data = {
        nombre,
        email,
        password,
        Tipo_idTipo: tipo,
      };

      if (id) {
        await fetch(`${API_URL_USUARIO}/${id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
      } else {
        await fetch(API_URL_USUARIO, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
      }

      form.reset();
      document.getElementById("usuarioId").value = "";
      cargarUsuarios();
    });

    cargarUsuarios();
  }, 100);
})();
