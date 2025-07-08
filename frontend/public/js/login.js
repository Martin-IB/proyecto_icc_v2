async function iniciarSesion(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const errorMsg = document.getElementById("error-msg");

  try {
    const response = await fetch("http://18.188.154.229:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      throw new Error("Credenciales incorrectas");
    }

    const usuario = await response.json();
    console.log("✅ Usuario autenticado:", usuario);

    // Guardar usuario en localStorage
    localStorage.setItem("usuario", JSON.stringify(usuario));

    // Ir al panel (único para todos)
    window.location.href = "/pages/panel_admin.html";

  } catch (error) {
    console.error("❌ Error al iniciar sesión:", error);
    errorMsg.textContent = "Correo o contraseña incorrectos.";
  }
}
