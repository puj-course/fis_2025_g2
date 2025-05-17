import { useState } from "react";
import { AuthService } from "../Services/AuthService";
import { useNavigate } from "react-router-dom";
import './Register.css';

export default function Register() {
  const [username, setUsername]   = useState("");
  const [email, setEmail]         = useState("");
  const [phone, setPhone]         = useState("");
  const [password, setPassword]   = useState("");
  const [confirm, setConfirm]     = useState("");
  const [isPremium, setIsPremium] = useState(false);
  const [error, setError]         = useState("");
  const [success, setSuccess]     = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (password !== confirm) {
      return setError("Las contraseñas no coinciden");
    }
    try {
      await AuthService.register({ username, email, phone, password, isPremium });
      setSuccess("Registrado correctamente. Redirigiendo al login...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="register-bg">
      <form onSubmit={handleSubmit} className="register-form">
        <h2>Registro</h2>

        <div>
          <label>Nombre de usuario</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Correo electrónico</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Teléfono</label>
          <input
            type="tel"
            value={phone}
            onChange={e => setPhone(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Confirmar Contraseña</label>
          <input
            type="password"
            value={confirm}
            onChange={e => setConfirm(e.target.value)}
            required
          />
        </div>

        <div className="flex items-center">
          <input
            id="premium"
            type="checkbox"
            checked={isPremium}
            onChange={e => setIsPremium(e.target.checked)}
          />
          <label htmlFor="premium">Cuenta Premium</label>
        </div>

        <button type="submit">Registrarse</button>

        {error && <p className="text-red-500">{error}</p>}
        {success && <p className="text-green-600">{success}</p>}
      </form>
    </div>
  );
}
