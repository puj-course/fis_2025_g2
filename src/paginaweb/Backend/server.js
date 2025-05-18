// backend/server.js
const express = require("express");
const cors = require("cors");
const auth = require("./authService");
const { sendTelegramMessage } = require("./telegramNotifier");

// ===== PATRÓN SINGLETON =====
class Server {
  static instance = null;
  
  constructor() {
    if (Server.instance) return Server.instance;
    
    this.app = express();
    this.app.use(cors());
    this.app.use(express.json());
    this.setupRoutes();
    
    Server.instance = this;
  }

  // ===== PATRÓN FACTORY METHOD =====
  createRouteHandler(type) {
    const handlers = {
      login: (req, res) => {
        const { username, password } = req.body;
        const user = auth.login(username, password);

        if (user) {
          sendTelegramMessage(`🔐 Login exitoso:\n• Usuario: ${username}`);
          const { password: pwd, ...userData } = user;
          res.json({ success: true, user: userData });
        } else {
          res.status(401).json({ success: false, message: "Credenciales inválidas" });
        }
      },
      register: (req, res) => {
        const { username, email, phone, password, isPremium } = req.body;
        const creado = auth.register(username, email, phone, password, isPremium);

        if (creado) {
          sendTelegramMessage(
            `🆕 Nuevo registro:\n• Usuario: ${username}\n• Email: ${email}\n• Teléfono: ${phone}\n• Premium: ${isPremium}`
          );
          res.json({ success: true, message: "Usuario creado exitosamente" });
        } else {
          res.status(400).json({ success: false, message: "El usuario ya existe" });
        }
      }
    };
    
    return handlers[type] || ((req, res) => res.status(404).send("Ruta no encontrada"));
  }

  // ===== PATRÓN MIDDLEWARE (Chain of Responsibility) =====
  applyMiddlewares() {
    this.app.use((req, res, next) => { // Logger middleware
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
    
    this.app.use((req, res, next) => { // Auth middleware
      if (req.path === '/login' || req.path === '/register') return next();
      // Lógica de autenticación para otras rutas
      next();
    });
  }

  setupRoutes() {
    this.applyMiddlewares();
    
    this.app.post("/login", this.createRouteHandler('login'));
    this.app.post("/register", this.createRouteHandler('register'));
  }

  start(port = 3001) {
    if (process.env.NODE_ENV !== 'test') {
      this.server = this.app.listen(port, () => {
        console.log(`Servidor backend en http://localhost:${port}`);
      });
    }
    return this.app;
  }

  stop() {
    if (this.server) this.server.close();
  }
}

// Uso del Singleton
const serverInstance = new Server();
const app = serverInstance.start();

// Exportar para pruebas
module.exports = { app, Server };