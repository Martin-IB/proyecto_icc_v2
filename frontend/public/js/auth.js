document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        showError("Por favor completa todos los campos.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("tipo", data.tipo);
            localStorage.setItem("nombre", data.nombre);
            localStorage.setItem("email", data.email);
            localStorage.setItem("id", data.id);
            window.location.href = "dashboard.html";
        } else {
            showError("⚠️ Credenciales incorrectas. Inténtalo de nuevo.");
        }
    } catch (error) {
        console.error("Error al iniciar sesión:", error);
        showError("❌ Error de conexión con el servidor.");
    }
});

function showError(message) {
    const errorMsg = document.getElementById("errorMsg");
    errorMsg.textContent = message;
    errorMsg.style.display = "block";
}
