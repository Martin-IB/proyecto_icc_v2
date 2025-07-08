
document.addEventListener("DOMContentLoaded", () => {
  cargarEstado();
  cargarGraficoTempHum();
  iniciarVoz()
});

async function cargarEstado() {
  try {
    const res = await fetch("http://18.188.154.229:8000/lectura"); // tu API ya existente
    let datos = await res.json();

    
    if (datos.length > 100) {
      datos = datos.slice(-100);
    }

    let ajuste = 0, optimo = 0, critico = 0;

    datos.forEach(dato => {
      if (dato.estado_ambiente === "Ajustar") ajuste++;
      else if (dato.estado_ambiente === "Óptimo") optimo++;
      else if (dato.estado_ambiente=== "Crítico") critico++;
    });

    const total = ajuste + optimo + critico;
    if (total === 0) return;

    const porcAjuste = Math.round((ajuste / total) * 100);
    const porcOptimo = Math.round((optimo / total) * 100);
    const porcCritico = Math.round((critico / total) * 100);

    crearGraficoCircular("ajusteChart", porcAjuste, "rgba(241, 196, 15, 0.8)");
    crearGraficoCircular("optimoChart", porcOptimo, "rgba(46, 204, 113, 0.8)");
    crearGraficoCircular("criticoChart", porcCritico, "rgba(231, 76, 60, 0.8)");
    mostrarPronostico(datos.slice(-100)); 

  } catch (error) {
    console.error("Error al cargar los datos del estado:", error);
  }
}

function crearGraficoCircular(idCanvas, porcentaje, color) {
  const ctx = document.getElementById(idCanvas).getContext("2d");

  const chart = new Chart(ctx, {
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
        const { width } = chart;
        const { height } = chart;
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

function mostrarPronostico(recientes) {
  let ajuste = 0, optimo = 0, critico = 0;

  recientes.forEach(dato => {
    const estado = dato.estado_ambiente;
    if (dato.estado_ambiente === "Ajustar") ajuste++;
    else if (dato.estado_ambiente === "Óptimo") optimo++;
    else if (dato.estado_ambiente=== "Crítico") critico++;
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





async function cargarGraficoTempHum() {
  try {
    const res = await fetch("http://18.188.154.229:8000/lectura");
    let datos = await res.json();

    if (datos.length > 100) {
      datos = datos.slice(-300);
    }

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
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
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
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
  
  } catch (error) {
    console.error("Error cargando datos de sensores:", error);
  }
}


// --- Control por voz e IA ---

let ultimaLectura = null;

// 🟩 Obtener la última lectura desde la API
async function obtenerUltimaLectura() {
  try {
    const res = await fetch("http://18.188.154.229:8000/lectura");
    const datos = await res.json();
    if (datos.length > 0) {
      ultimaLectura = datos[datos.length - 1]; // Último elemento
    }
  } catch (error) {
    console.error("Error obteniendo lectura:", error);
  }
}

// 🟦 Función principal: escucha y procesa comando
function iniciarVoz() {
  const reconocimiento = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  reconocimiento.lang = "es-ES";
  reconocimiento.interimResults = false;
  reconocimiento.maxAlternatives = 1;

  reconocimiento.start();

  reconocimiento.onresult = async (event) => {
    const comando = event.results[0][0].transcript;
    await obtenerUltimaLectura(); // Obtener dato más reciente
    interpretarComando(comando);
  };

  reconocimiento.onerror = (e) => {
    hablar("Hubo un error al reconocer tu voz.");
    console.error("Error de voz:", e);
  };
}

// 🟨 Procesamiento del comando de voz (intenciones básicas)
function interpretarComando(texto) {
  const textoNormalizado = texto.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); // quita tildes

  const comandos = [
    {
      patrones: ["pronostico", "ambiente", "condiciones", "estado del sistema", "como esta"],
      accion: responderPronostico
    },
    {
      patrones: ["riego", "regar", "riego necesario", "regar hongos", "necesita agua"],
      accion: responderPronostico
    },
    {
      patrones: ["temperatura", "calor", "esta caliente", "que temperatura hay"],
      accion: responderTemperatura
    },
    {
      patrones: ["humedad", "seco", "humedo", "cuanta humedad"],
      accion: responderHumedad
    }
  ];

  for (const cmd of comandos) {
    if (cmd.patrones.some(p => textoNormalizado.includes(p))) {
      cmd.accion();
      return;
    }
  }

  hablar("");
}


// 🟥 Funciones de respuesta

async function responderPronostico() {
  try {
    const res = await fetch("http://18.188.154.229:8000/lectura");
    const datos = await res.json();
    const ultimos100 = datos.slice(-100); // Últimas 100 lecturas

    let ajuste = 0, optimo = 0, critico = 0;

    ultimos100.forEach(dato => {
      const estado = dato.estado_ambiente?.toLowerCase();
      if (dato.estado_ambiente === "Ajustar") ajuste++;
      else if (dato.estado_ambiente === "Óptimo") optimo++;
      else if (dato.estado_ambiente=== "Crítico") critico++;
    });

    // Elegir el estado predominante
    const maximo = Math.max(ajuste, optimo, critico);
    let mensaje = "";

    if (maximo === critico) {
      mensaje = " El control del biorrector está en estado crítico. Deberías revisar los sensores y agregar sustrato ahora.";
    } else if (maximo === ajuste) {
      mensaje = "El control del biorrector necesita ajustes de los sensores de humedad y temperatura.";
    } else if (maximo === optimo) {
      mensaje = " El biorreactor está en condiciones óptimas, mide el nivel de sustrato en los hongos.";
    } else {
      mensaje = "No pude determinar el estado del sistema con los datos actuales.";
    }

    hablar(mensaje);

  } catch (error) {
    console.error("Error en el pronóstico:", error);
    hablar("No se pudo obtener el pronóstico del sistema.");
  }
}


function responderTemperatura() {
  if (ultimaLectura) {
    hablar(`La temperatura actual en el biorrector es de ${ultimaLectura.temperatura.toFixed(1)} °`);
  } else {
    hablar("No tengo información de temperatura.");
  }
}

function responderHumedad() {
  if (ultimaLectura) {
    hablar(`La humedad actual en el biorrector es de ${ultimaLectura.humedad.toFixed(1)} %`);
  } else {
    hablar("No tengo información de humedad.");
  }
}

//Leer en voz alta + mostrar en pantalla
function hablar(mensaje) {
  const outputFlotante = document.getElementById("mensajeAsistente");
  const outputTarjeta = document.getElementById("comandoReconocido");

  // Mostrar en flotante
  if (outputFlotante) {
    outputFlotante.innerText = mensaje;
    outputFlotante.style.display = "block";
    setTimeout(() => {
      outputFlotante.style.display = "none";
    }, 5000);
  }

  // Mostrar en tarjeta (si existe)
  if (outputTarjeta) {
    outputTarjeta.innerText = mensaje;
  }

  // Leer en voz alta
  const synth = window.speechSynthesis;
  synth.cancel();
  const voz = new SpeechSynthesisUtterance(mensaje);
  voz.lang = "es-ES";
  synth.speak(voz);
}






