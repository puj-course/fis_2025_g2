// src/views/Prediccion.jsx
import { useState } from "react";
import { PredictionService } from "../Services/PredictionService";
import { motion } from "framer-motion";
import './Prediccion.css';

export default function Prediccion() {
  const [producto, setProducto] = useState("arroz");
  const [tienda, setTienda] = useState("Exito");
  const [isPremium, setIsPremium] = useState(false);
  const [horizon, setHorizon] = useState(1);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    setError("");
    try {
      const resp = await PredictionService.predict({
        producto,
        tienda,
        is_premium: isPremium,
        horizon_days: horizon
      });
      setResultado(resp.prediction);
    } catch (e) {
      setError(e.message);
    }
  };

  const container = { hidden: {}, show: { transition: { staggerChildren: 0.1 } } };
  const item = { hidden: { opacity: 0, y: 20 }, show: { opacity: 1, y: 0 } };

  return (
    <div className="full-screen flex-center bg-gradient">
      <motion.div
        className="pred-glass"
        variants={container}
        initial="hidden"
        animate="show"
      >
        <motion.h2 variants={item} className="logo-text">
          Predicción de Precios
        </motion.h2>

        <motion.div variants={item} className="form-stack">
          <label>Producto</label>
          <select
            value={producto}
            onChange={e => setProducto(e.target.value)}
          >
            <option value="arroz">Arroz</option>
            <option value="azucar">Azúcar</option>
            <option value="leche">Leche</option>
            <option value="Huevo">Huevo</option>
            <option value="aceite">Aceite</option>
          </select>
        </motion.div>

        <motion.div variants={item} className="form-stack">
          <label>Tienda</label>
          <input
            type="text"
            value={tienda}
            onChange={e => setTienda(e.target.value)}
          />
        </motion.div>

        <motion.div variants={item} className="form-stack checkbox-stack">
          <input
            id="premium"
            type="checkbox"
            checked={isPremium}
            onChange={e => setIsPremium(e.target.checked)}
          />
          <label htmlFor="premium">Cuenta Premium</label>
        </motion.div>

        <motion.div variants={item} className="form-stack">
          <label>Días al futuro</label>
          <input
            type="number"
            value={horizon}
            onChange={e => setHorizon(+e.target.value)}
            min={1}
          />
        </motion.div>

        <motion.button
          variants={item}
          onClick={handlePredict}
          className="btn-primary"
        >
          Predecir
        </motion.button>

        {resultado !== null && (
          <motion.p variants={item} className="success-text">
            Predicción: ${resultado}
          </motion.p>
        )}
        {error && (
          <motion.p variants={item} className="error-text">
            {error}
          </motion.p>
        )}
      </motion.div>
    </div>
  );
}


