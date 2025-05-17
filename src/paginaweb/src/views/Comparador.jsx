// src/views/Comparador.jsx
import React, { useState } from "react";
import { PredictionService } from "../Services/PredictionService";

const PRODUCT_ALIASES = [
  "arroz",
  "azucar",
  "aceite",
  "huevos",
  "leche",
  "pan",
  "papa",
  "frijol",
];

export default function Comparador() {
  // Leer usuario logueado
  const stored = localStorage.getItem("user");
  const currentUser = stored ? JSON.parse(stored) : null;
  const isPremium = currentUser?.isPremium || false;

  // estados de predicción
  const [productoPred, setProductoPred] = useState("arroz");
  const [tiendaPred, setTiendaPred] = useState("Exito");
  const [horizon, setHorizon] = useState(1);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    setError("");
    setResultado(null);
    try {
      const resp = await PredictionService.predict({
        producto: productoPred,
        tienda: tiendaPred,
        is_premium: isPremium,
        horizon_days: horizon,
      });
      setResultado(resp.prediction);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen p-8 bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Predicción de Precios 🔮
        </h2>

        <div className="space-y-4">
          {/* Producto */}
          <div>
            <label className="block font-medium mb-1">Producto:</label>
            <select
              className="w-full border rounded px-2 py-1"
              value={productoPred}
              onChange={(e) => setProductoPred(e.target.value)}
            >
              {PRODUCT_ALIASES.map((alias) => (
                <option key={alias} value={alias}>
                  {alias.charAt(0).toUpperCase() + alias.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Tienda */}
          <div>
            <label className="block font-medium mb-1">Tienda:</label>
            <input
              type="text"
              className="w-full border rounded px-2 py-1"
              value={tiendaPred}
              onChange={(e) => setTiendaPred(e.target.value)}
            />
          </div>

          {/* Horizon */}
          <div>
            <label className="block font-medium mb-1">Días al futuro:</label>
            <input
              type="number"
              min={1}
              className="w-full border rounded px-2 py-1"
              value={horizon}
              onChange={(e) => setHorizon(+e.target.value)}
            />
          </div>

          {/* Botón */}
          <button
            onClick={handlePredict}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded"
          >
            Predecir
          </button>

          {/* Resultado / Error */}
          {resultado !== null && (
            <p className="mt-4 text-xl text-center">
              Predicción:&nbsp;
              <span className="font-bold">${resultado.toLocaleString()}</span>
            </p>
          )}
          {error && (
            <p className="mt-2 text-red-500 text-center font-medium">
              Error: {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
