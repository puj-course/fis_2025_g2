// src/views/Login.jsx
import { useState } from "react";
import { AuthService } from "../Services/AuthService";
import { useNavigate, Link } from "react-router-dom";
import { motion } from "framer-motion";
import "./Login.css";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const user = await AuthService.login(username, password);
      if (user.isPremium) navigate("/prediccion");
      else navigate("/comparador");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const container = {
    hidden: {},
    show: { transition: { staggerChildren: 0.1 } }
  };
  const item = {
    hidden: { opacity: 0, y: 20 },
    show:   { opacity: 1, y: 0 }
  };

  return (
    <div className="bg-gradient full-screen flex-center">
      <motion.div
        className="login-glass"
        variants={container}
        initial="hidden"
        animate="show"
      >
        <motion.h2 variants={item} className="logo-text">
          Feedback
        </motion.h2>
        <motion.p variants={item} className="subtitle">
          Predicción de precios de la canasta familiar
        </motion.p>

        <motion.form
          onSubmit={handleSubmit}
          className="form-stack"
          variants={item}
        >
          <label htmlFor="username">Usuario</label>
          <motion.input
            variants={item}
            id="username"
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            placeholder="Ingresa tu usuario"
            required
          />

          <label htmlFor="password">Contraseña</label>
          <motion.input
            variants={item}
            id="password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="Ingresa tu contraseña"
            required
          />

          <motion.button
            variants={item}
            type="submit"
            className="btn-primary"
            disabled={loading}
          >
            {loading
              ? <span className="spinner"></span>
              : "Ingresar"}
          </motion.button>
        </motion.form>

        {error && (
          <motion.p variants={item} className="error-text">
            {error}
          </motion.p>
        )}

        <motion.p variants={item} className="register-text">
          ¿No tienes cuenta?{" "}
          <Link to="/register">Regístrate</Link>
        </motion.p>
      </motion.div>
    </div>
  );
}
