
document.addEventListener("DOMContentLoaded", () => {
  cargarEstado();
  cargarGraficoTempHum();
  iniciarVoz();
});


// Carga y calcula el estado general del biorreactor
async function cargarEstado() {
  try {
    //const res = await fetch("http://3.132.200.37:8000/lectura"); 
    const res = await fetch("http://localhost:8000/lectura");
    let datos = await res.json();
    if (datos.length > 100) datos = datos.slice(-100);

    let ajuste = 0, optimo = 0, critico = 0;
    datos.forEach(dato => {
      if (dato.estado_ambiente === "Ajustar") ajuste++;
      else if (dato.estado_ambiente === "Óptimo") optimo++;
      else if (dato.estado_ambiente === "Crítico") critico++;
    });

    const total = ajuste + optimo + critico;
    if (total === 0) return;

    crearGraficoCircular("ajusteChart", Math.round((ajuste / total) * 100), "rgba(241, 196, 15, 0.8)");
    crearGraficoCircular("optimoChart", Math.round((optimo / total) * 100), "rgba(46, 204, 113, 0.8)");
    crearGraficoCircular("criticoChart", Math.round((critico / total) * 100), "rgba(231, 76, 60, 0.8)");

    mostrarPronostico(datos);
    generarRecomendaciones(datos);

  } catch (error) {
    console.error("Error al cargar los datos del estado:", error);
  }
}



// Gráfico circular para cada estado
function crearGraficoCircular(idCanvas, porcentaje, color) {
  const ctx = document.getElementById(idCanvas).getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Estado", "Resto"],
      datasets: [{
        data: [porcentaje, 100 - porcentaje],
        backgroundColor: [color, "#ecf0f1"],
        borderWidth: 1
      }]
    },
    options: {
      cutout: "70%",
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    },
    plugins: [{
      id: 'textInCenter',
      beforeDraw(chart) {
        const { width, height } = chart;
        const ctx = chart.ctx;
        ctx.restore();
        const fontSize = (height / 5).toFixed(2);
        ctx.font = fontSize + "px Arial";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "#2c3e50";
        const text = `${porcentaje}%`;
        const textX = Math.round((width - ctx.measureText(text).width) / 2);
        const textY = height / 2;
        ctx.fillText(text, textX, textY);
        ctx.save();
      }
    }]
  });
}

// Muestra el pronóstico principal en texto
function mostrarPronostico(recientes) {
  let ajuste = 0, optimo = 0, critico = 0;
  recientes.forEach(dato => {
    if (dato.estado_ambiente === "Ajustar") ajuste++;
    else if (dato.estado_ambiente === "Óptimo") optimo++;
    else if (dato.estado_ambiente === "Crítico") critico++;
  });

  const container = document.getElementById("pronosticoContainer");
  const mensaje = document.getElementById("pronosticoRiego");

  container.classList.remove("critico", "ajustar", "optimo");
  if (critico > ajuste && critico > optimo) {
    mensaje.textContent = "Ambiente crítico. Agrega sustrato y revisa sensores.";
    container.classList.add("critico");
  } else if (ajuste > critico && ajuste > optimo) {
    mensaje.textContent = "Ambiente requiere ajuste. Revisa temperatura o humedad.";
    container.classList.add("ajustar");
  } else if (optimo > ajuste && optimo > critico) {
    mensaje.textContent = "Condiciones óptimas. No se requieren acciones.";
    container.classList.add("optimo");
  } else {
    mensaje.textContent = "Condiciones variables. Sigue monitoreando.";
  }
}



// Gráficos de temperatura y humedad
async function cargarGraficoTempHum() {
  try {
    const res = await fetch("http://3.132.200.37:8000/lectura");
    //const res = await fetch("http://localhost:8000/lectura");
    let datos = await res.json();
    if (datos.length > 300) datos = datos.slice(-300);

    const labels = datos.map(d => d.idLectura_sensores);
    const tempData = datos.map(d => d.temperatura);
    const humData = datos.map(d => d.humedad);

    const ctxTemp = document.getElementById("graficoTemp").getContext("2d");
    const ctxHum = document.getElementById("graficoHum").getContext("2d");

    new Chart(ctxTemp, {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "Temperatura (°C)",
          data: tempData,
          borderColor: "rgba(255, 99, 132, 1)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });

    new Chart(ctxHum, {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: "Humedad (%)",
          data: humData,
          borderColor: "rgba(54, 162, 235, 1)",
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          tension: 0.4,
          fill: false,
          pointRadius: 0
        }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
  } catch (error) {
    console.error("Error cargando datos de sensores:", error);
  }
}


// Nuevo: gráfico de pronóstico diario (óptimo/ajuste/crítico)
async function cargarGraficoPronostico() {
  try {
    const res = await fetch("http://3.132.200.37:8000/lectura");
    //const res = await fetch("http://localhost:8000/lectura");
    let datos = await res.json();

    if (datos.length < 10) return;

    const resumen = {};
    datos.forEach(d => {
      const fecha = d.fecha.slice(0, 10);
      if (!resumen[fecha]) resumen[fecha] = { Optimo: 0, Ajustar: 0, Critico: 0 };

      if (d.estado_ambiente === "Óptimo") resumen[fecha].Optimo++;
      else if (d.estado_ambiente === "Ajustar") resumen[fecha].Ajustar++;
      else if (d.estado_ambiente === "Crítico") resumen[fecha].Critico++;
    });

    const fechas = Object.keys(resumen);
    const dataOptimo = fechas.map(f => resumen[f].Optimo);
    const dataAjuste = fechas.map(f => resumen[f].Ajustar);
    const dataCritico = fechas.map(f => resumen[f].Critico);

    const ctx = document.getElementById("graficoPronostico").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: fechas,
        datasets: [
          {
            label: "Óptimo",
            data: dataOptimo,
            backgroundColor: "rgba(46, 204, 113, 0.7)"
          },
          {
            label: "Ajustar",
            data: dataAjuste,
            backgroundColor: "rgba(241, 196, 15, 0.7)"
          },
          {
            label: "Crítico",
            data: dataCritico,
            backgroundColor: "rgba(231, 76, 60, 0.7)"
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "top" },
          title: {
            display: true,
            text: "Pronóstico Diario por Estado del Ambiente"
          }
        }
      }
    });
  } catch (error) {
    console.error("Error al cargar pronóstico diario:", error);
  }
}





// --- Control por Voz e IA Mejorado ---

let ultimaLectura = null;

// Obtener la última lectura desde la API
async function obtenerUltimaLectura() {
  try {
    //const res = await fetch("http://localhost:8000/lectura");
    const res = await fetch("http://3.132.200.37:8000/lectura");
    const datos = await res.json();
    if (datos.length > 0) {
      ultimaLectura = datos[datos.length - 1];
      localStorage.setItem("ultimaLectura", JSON.stringify({
        data: ultimaLectura,
        timestamp: Date.now()
      }));
    }
  } catch (error) {
    console.error("Error obteniendo lectura:", error);
  }
}

// Procesamiento principal: escucha y procesa comandos de voz
function iniciarVoz() {
  const reconocimiento = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  reconocimiento.lang = "es-ES";
  reconocimiento.interimResults = false;
  reconocimiento.maxAlternatives = 1;

  reconocimiento.start();

  reconocimiento.onresult = async (event) => {
    const comando = event.results[0][0].transcript;
    await obtenerUltimaLectura();
    interpretarComando(comando);
  };

  reconocimiento.onerror = (e) => {
    hablar("Hubo un error al reconocer tu voz.");
    console.error("Error de voz:", e);
  };
}

// Comparación básica para mejorar coincidencias de comandos
function similaridad(p1, p2) {
  const a = new Set(p1.split(" "));
  const b = new Set(p2.split(" "));
  const inter = new Set([...a].filter(x => b.has(x)));
  return inter.size / Math.max(a.size, b.size);
}

// Interpretar comandos por voz
function interpretarComando(texto) {
  const textoNormalizado = texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

  const comandos = [
    { patrones: ["pronostico", "ambiente", "estado del sistema", "como esta"], accion: responderPronostico },
    { patrones: ["riego", "regar", "necesita agua"], accion: responderPronostico },
    { patrones: ["temperatura", "calor", "que temperatura"], accion: responderTemperatura },
    { patrones: ["humedad", "seco", "humedo"], accion: responderHumedad },
    { patrones: ["pronostico del dia", "clima", "como estara"], accion: pronosticoDelDia }
  ];

  for (const cmd of comandos) {
    if (cmd.patrones.some(p => similaridad(p, textoNormalizado) > 0.5)) {
      cmd.accion();
      registrarComando(texto);
      return;
    }
  }

  hablar("No comprendí el comando.");
  registrarComando(texto);
}

function generarRespuesta(base, dato) {
  const respuestas = [
    `${base} El valor actual es ${dato}.`,
    `Actualmente tenemos ${dato} en ${base.toLowerCase()}.`,
    `Actualmente tenemos ${dato} de ${base.toLowerCase()}.`
  ];
  return respuestas[Math.floor(Math.random() * respuestas.length)];
}

async function responderPronostico() {
  try {
    //const res = await fetch("http://localhost:8000/lectura");
    const res = await fetch("http://3.132.200.37:8000/lectura");
    const datos = await res.json();
    const ultimos = datos.slice(-100);

    let ajuste = 0, optimo = 0, critico = 0;
    ultimos.forEach(d => {
      const estado = d.estado_ambiente?.toLowerCase();
      if (estado === "ajustar") ajuste++;
      else if (estado === "\u00f3ptimo") optimo++;
      else if (estado === "cr\u00edtico") critico++;
    });

    let mensaje = "";
    const max = Math.max(ajuste, optimo, critico);
    if (max === critico) mensaje = "Estado crítico. Revisa sensores y sustrato";
    else if (max === ajuste) mensaje = "Necesita ajustes en sensores";
    else if (max === optimo) mensaje = "Condiciones óptimas";
    else mensaje = "No se pudo determinar el estado actual";

    hablar(mensaje);
  } catch (err) {
    console.error("Error en pronóstico:", err);
    hablar("Error al obtener el pronóstico actual");
  }
}

function responderTemperatura() {
  if (ultimaLectura) {
    const mensaje = generarRespuesta("Temperatura", `${ultimaLectura.temperatura} °`);
    hablar(mensaje);
  } else {
    hablar("No tengo información actual de temperatura");
  }
}

function responderHumedad() {
  if (ultimaLectura) {
    const mensaje = generarRespuesta("Humedad", `${ultimaLectura.humedad}%`);
    hablar(mensaje);
  } else {
    hablar("No tengo información actual de humedad");
  }
}

// Predicción del día con heurística
async function pronosticoDelDia() {
  try {
    //const res = await fetch("http://localhost:8000/lectura");
    const res = await fetch("http://3.132.200.37:8000/lectura");
    const datos = await res.json();
    const ultimos = datos.slice(-200);

    let temp = 0, hum = 0;
    ultimos.forEach(d => {
      temp += parseFloat(d.temperatura);
      hum += parseFloat(d.humedad);
    });

    const promTemp = temp / ultimos.length;
    const promHum = hum / ultimos.length;
    let mensaje = "";

    if (promTemp > 30) mensaje += "Temperaturas altas, supervisar el sistema";
    else if (promTemp < 20) mensaje += "Temperatura baja, posible lentitud en cultivo ";
    else mensaje += "Temperatura estable,";

    if (promHum > 80) mensaje += "Alta humedad, revisar ventilación.";
    else if (promHum < 40) mensaje += "Humedad baja, revisar el sistema de riego.";
    else mensaje += "Humedad adecuada.";

    hablar(mensaje);
  } catch (err) {
    console.error("Error en pronóstico diario:", err);
    hablar("No se pudo obtener el pronóstico del día.");
  }
}

function hablar(mensaje) {
  const outputFlotante = document.getElementById("mensajeAsistente");
  const outputTarjeta = document.getElementById("comandoReconocido");

  if (outputFlotante) {
    outputFlotante.innerText = mensaje;
    outputFlotante.style.display = "block";
    setTimeout(() => outputFlotante.style.display = "none", 5000);
  }

  if (outputTarjeta) {
    outputTarjeta.innerText = mensaje;
  }

  const synth = window.speechSynthesis;
  synth.cancel();
  const voz = new SpeechSynthesisUtterance(mensaje);
  voz.lang = "es-ES";
  synth.speak(voz);
}

// Registrar comando en la base de datos
async function registrarComando(comando) {
  try {
    await fetch("http://3.132.200.37:8000/registro", {
    //await fetch("http://localhost:8000/registro", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tipo_evento: "Voz",
        description: comando,
        Usuario_idUsuario: 1, 
        Biorreactor_idBiorreactor: 1, 
        Sensores_idSensores: 1 
      })
    });
  } catch (error) {
    console.error("Error registrando comando:", error);
  }
} 

function generarRecomendaciones(datos) {
  const recomendaciones = [];

   const ultimos = datos.slice(-50);

  const promedioTemp = ultimos.reduce((s, d) => s + d.temperatura, 0) / ultimos.length;
  const promedioHum = ultimos.reduce((s, d) => s + d.humedad, 0) / ultimos.length;

  if (promedioTemp > 28) {
    recomendaciones.push("La temperatura está alta, verifica ventilación del biorreactor.");
  }
  if (promedioHum < 60) {
    recomendaciones.push("Niveles de humedad bajos. Considera iniciar un ciclo de riego.");
  }

  else {
    recomendaciones.push("Todo está funcionando correctamente. No se requieren ajustes.");
  }

  const ul = document.getElementById("listaRecomendaciones");
  ul.innerHTML = "";
  recomendaciones.forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    ul.appendChild(li);
  });
}








