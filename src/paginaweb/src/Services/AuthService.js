// src/Services/AuthService.js

export const AuthService = {
  async login(nombreUsuario, contrasena) {
    const res = await fetch("http://localhost:3001/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nombreUsuario, contrasena }),
    });

    if (!res.ok) {
      throw new Error("Credenciales inválidas");
    }

    const data = await res.json();
    return data.user;
  },

  async registrar(nombreUsuario, contrasena) {
    const res = await fetch("http://localhost:3001/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ nombreUsuario, contrasena }),
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Error al registrar");
    }

    return data;
  },
};
