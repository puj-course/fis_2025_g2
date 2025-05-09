// backend/server.js
const express = require("express");
const cors = require("cors");
const auth = require("./authService");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/login", (req, res) => {
  const { nombreUsuario, contrasena } = req.body;
  const user = auth.login(nombreUsuario, contrasena);
  if (user) {
    res.json({ success: true, user });
  } else {
    res.status(401).json({ success: false, message: "Credenciales inválidas" });
  }
});

app.post("/register", (req, res) => {
  const { nombreUsuario, contrasena } = req.body;
  const creado = auth.register(nombreUsuario, contrasena);
  if (creado) {
    res.json({ success: true, message: "Usuario creado exitosamente" });
  } else {
    res.status(400).json({ success: false, message: "El usuario ya existe" });
  }
});

app.listen(3001, () => console.log("Servidor backend en http://localhost:3001"));
