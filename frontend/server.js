const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000; // Puedes cambiar el puerto si lo deseas

// Middleware para servir archivos estáticos desde la carpeta "public"
app.use(express.static(path.join(__dirname, 'public')));

// Redirigir "/" al login o index
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Servidor frontend corriendo en http://18.188.154.229/${PORT}`);
});
