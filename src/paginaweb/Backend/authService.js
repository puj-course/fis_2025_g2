// backend/authService.js
const fs = require("fs");
const path = require("path");

const usuariosPath = path.join(__dirname, "usuarios.txt");

// Lee y parsea el archivo usuarios.txt
function leerUsuarios() {
  if (!fs.existsSync(usuariosPath)) return [];
  return fs.readFileSync(usuariosPath, "utf-8")
    .split("\n")
    .filter(Boolean)
    .map(linea => {
      const [username, email, phone, password, isPremium] = linea.split(",");
      return {
        username,
        email,
        phone,
        password,
        isPremium: isPremium === "true"
      };
    });
}

// Registra un usuario; devuelve false si el username ya existe
function register(username, email, phone, password, isPremium) {
  const usuarios = leerUsuarios();
  if (usuarios.some(u => u.username === username)) return false;
  const linea = `${username},${email},${phone},${password},${isPremium}\n`;
  fs.appendFileSync(usuariosPath, linea, "utf-8");
  return true;
}

// Valida login por username + password y devuelve el objeto usuario
function login(username, password) {
  const usuarios = leerUsuarios();
  return usuarios.find(u =>
    u.username === username && u.password === password
  ) || null;
}

module.exports = { leerUsuarios, register, login };
