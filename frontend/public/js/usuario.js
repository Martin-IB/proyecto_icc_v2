const API_URL = "http://localhost:8000/usuario";

document.addEventListener("DOMContentLoaded", () => {
  // Esperamos unos milisegundos para asegurarnos que el HTML dinámico ya se ha renderizado
  setTimeout(() => {
    console.log("👤 Módulo usuario.js cargado");

    const form = document.getElementById("usuarioForm");
    const nombreInput = document.getElementById("nombre");
    const emailInput = document.getElementById("email");
    const usuarioIdInput = document.getElementById("usuarioId");
    const tableBody = document.getElementById("usuarioTableBody");

    if (!form || !nombreInput || !emailInput || !usuarioIdInput || !tableBody) {
      console.warn("⚠️ Elementos de formulario no encontrados. Revisa que usuario.html se haya cargado correctamente.");
      return;
    }

    cargarUsuarios();

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const nombre = nombreInput.value;
      const email = emailInput.value;
      const id = usuarioIdInput.value;
      const data = { nombre, email };

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
      usuarioIdInput.value = "";
      cargarUsuarios();
    });

    async function cargarUsuarios() {
      try {
        const res = await fetch(API_URL);
        const usuarios = await res.json();

        tableBody.innerHTML = "";

        usuarios.forEach(u => {
          const row = document.createElement("tr");

          row.innerHTML = `
            <td>${u.id}</td>
            <td>${u.nombre}</td>
            <td>${u.email}</td>
            <td>${u.fecha_registro?.split("T")[0] || ""}</td>
            <td>
              <button class="btn btn-warning btn-sm" onclick="editarUsuario(${u.id}, '${u.nombre}', '${u.email}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarUsuario(${u.id})">Eliminar</button>
            </td>
          `;

          tableBody.appendChild(row);
        });
      } catch (err) {
        console.error("❌ Error al cargar usuarios:", err);
      }
    }

    window.editarUsuario = function (id, nombre, email) {
      nombreInput.value = nombre;
      emailInput.value = email;
      usuarioIdInput.value = id;
    };

    window.eliminarUsuario = async function (id) {
      if (confirm("¿Estás seguro de eliminar este usuario?")) {
        await fetch(`${API_URL}/${id}`, {
          method: "DELETE"
        });
        cargarUsuarios();
      }
    };
  }, 300); // espera mínima para asegurar que HTML ya fue cargado dinámicamente
});
