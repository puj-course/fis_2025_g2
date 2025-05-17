// src/Services/AuthService.js
const API = "http://localhost:3001";

export const AuthService = {
  async register({ username, email, phone, password, isPremium }) {
    const res = await fetch(`${API}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, phone, password, isPremium }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Error al registrar");
    return data;
  },

  async login(username, password) {
    const res = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Credenciales inválidas");
    // guarda en localStorage
    localStorage.setItem("user", JSON.stringify(data.user));
    return data.user;
  },
};
