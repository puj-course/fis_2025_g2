const API = "http://localhost:8000";

export const PredictionService = {
  async predict({ producto, tienda, is_premium, horizon_days = 1 }) {
    const res = await fetch(`${API}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ producto, tienda, is_premium, horizon_days }),
    });
    if (!res.ok) {
      const { detail } = await res.json();
      throw new Error(detail || "Error al predecir");
    }
    return await res.json();
  },
};
