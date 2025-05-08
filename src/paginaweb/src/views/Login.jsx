import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthService } from "../Services/AuthService";

export default function Login() {
  const [nombreUsuario, setNombreUsuario] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const usuario = await AuthService.login(nombreUsuario, contrasena);

    if (usuario) {
      setError("");
      navigate("/"); // Cambia la ruta a donde quieras ir tras iniciar sesión
    } else {
      setError("Nombre de usuario o contraseña incorrectos.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", marginTop: "50px" }}>
      <h2>Iniciar Sesión</h2>
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
        <button type="submit">Ingresar</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Enlace al registro (Paso 3 que mencionaste) */}
      <p style={{ marginTop: "10px" }}>
        ¿No tienes cuenta? <Link to="/register">Regístrate aquí</Link>
      </p>
    </div>
  );
}
