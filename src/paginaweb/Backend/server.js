// backend/server.js
const express = require("express");
const cors = require("cors");
const auth = require("./authService");
const { sendTelegramMessage } = require("./telegramNotifier");

const app = express();
app.use(cors());
app.use(express.json());

// Ruta de login
app.post("/login", (req, res) => {
  const { username, password } = req.body;
  const user = auth.login(username, password);

  if (user) {
    // Enviar notificación a Telegram
    sendTelegramMessage(`🔐 Login exitoso:\n• Usuario: ${username}`);

    // No mandamos la password en la respuesta
    const { password: pwd, ...sinPass } = user;
    res.json({ success: true, user: sinPass });
  } else {
    res.status(401).json({ success: false, message: "Credenciales inválidas" });
  }
});

// Ruta de registro
app.post("/register", (req, res) => {
  const { username, email, phone, password, isPremium } = req.body;
  const creado = auth.register(username, email, phone, password, isPremium);

  if (creado) {
    // Enviar notificación a Telegram
    sendTelegramMessage(
      `🆕 Nuevo registro:\n• Usuario: ${username}\n• Email: ${email}\n• Teléfono: ${phone}\n• Premium: ${isPremium}`
    );

    res.json({ success: true, message: "Usuario creado exitosamente" });
  } else {
    res
      .status(400)
      .json({ success: false, message: "El usuario ya existe" });
  }
});

// Levantar servidor
app.listen(3001, () =>
  console.log("Servidor backend en http://localhost:3001")
);
