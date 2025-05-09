// backend/authService.js
const fs = require("fs");
const path = require("path");

const usuariosPath = path.join(__dirname, "usuarios.txt");

function leerUsuarios() {
  if (!fs.existsSync(usuariosPath)) return [];
  const data = fs.readFileSync(usuariosPath, "utf-8");
  return data
    .split("\n")
    .filter(linea => linea)
    .map(linea => {
      const [nombreUsuario, contrasena] = linea.split(",");
      return { nombreUsuario, contrasena };
    });
}

function guardarUsuario(usuario) {
  const linea = `${usuario.nombreUsuario},${usuario.contrasena}\n`;
  fs.appendFileSync(usuariosPath, linea, "utf-8");
}

function login(nombreUsuario, contrasena) {
  const usuarios = leerUsuarios();
  return usuarios.find(
    (u) => u.nombreUsuario === nombreUsuario && u.contrasena === contrasena
  );
}

function register(nombreUsuario, contrasena) {
  const usuarios = leerUsuarios();
  const existe = usuarios.some((u) => u.nombreUsuario === nombreUsuario);
  if (existe) return false;
  guardarUsuario({ nombreUsuario, contrasena });
  return true;
}

module.exports = {
  login,
  register,
};
