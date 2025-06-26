document.addEventListener("DOMContentLoaded", () => {
    const nombre = localStorage.getItem("nombre");
    const tipo = localStorage.getItem("tipo");

    if (!nombre || !tipo) {
        alert("Debe iniciar sesión primero.");
        window.location.href = "index.html";
        return;
    }

    document.getElementById("username").innerText = nombre;

    const adminSection = document.getElementById("adminMenu");
    if (tipo !== "admin") {
        adminSection.style.display = "none";
    }

    document.getElementById("logoutBtn").addEventListener("click", () => {
        localStorage.clear();
        window.location.href = "index.html";
    });

    // Guardar contenido original del panel
    const main = document.getElementById("mainContent");
    if (main) {
        window._originalContent = main.innerHTML;
    }

    // Manejar clics en los enlaces del menú
    document.querySelectorAll(".menu-link").forEach(link => {
        link.addEventListener("click", async (e) => {
            e.preventDefault();
            const url = link.dataset.url;

            if (url === "panel") {
                document.getElementById("mainContent").innerHTML = window._originalContent;
                return;
            }

            try {
                const res = await fetch(url);
                const htmlText = await res.text();

                const tempDom = document.createElement("div");
                tempDom.innerHTML = htmlText;

                const bodyContent = tempDom.querySelector("body")?.innerHTML || htmlText;
                document.getElementById("mainContent").innerHTML = bodyContent;

                // Cargar JS dinámico
                cargarScriptDinamico(url);

            } catch (error) {
                console.error("Error al cargar módulo:", error);
                document.getElementById("mainContent").innerHTML = "<p>Error al cargar el contenido.</p>";
            }
        });
    });
});

function cargarScriptDinamico(rutaHtml) {
    const nombreArchivo = rutaHtml.split("/").pop().replace(".html", "");
    const rutaScript = `js/${nombreArchivo}.js`;

    const script = document.createElement("script");
    script.src = rutaScript;
    script.defer = true;
    document.body.appendChild(script);
}
