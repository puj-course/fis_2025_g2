import { useState } from "react";
import { AuthService } from "../Services/AuthService";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [nombreUsuario, setNombreUsuario] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");
  const [exito, setExito] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setExito("");

    try {
      await AuthService.registrar(nombreUsuario, contrasena);
      setExito("Usuario registrado correctamente. Redirigiendo...");
      setTimeout(() => navigate("/login"), 2000); // Redirige tras 2 segundos
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", marginTop: "50px" }}>
      <h2>Registro</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Nombre de usuario:</label>
          <input
            type="text"
            value={nombreUsuario}
            onChange={(e) => setNombreUsuario(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            required
          />
        </div>
        <button type="submit">Registrarse</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {exito && <p style={{ color: "green" }}>{exito}</p>}
    </div>
  );
}
