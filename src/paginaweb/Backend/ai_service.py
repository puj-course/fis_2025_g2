from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from Backend.IA import predict_price_free, predict_price_premium
from Backend.notify import send_telegram

app = FastAPI()

# --- Configuración de CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # o lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, OPTIONS, etc.
    allow_headers=["*"],        # Content-Type, Authorization, etc.
)

class PredictRequest(BaseModel):
    producto: str
    tienda: str
    is_premium: bool
    horizon_days: Optional[int] = 1

class PredictResponse(BaseModel):
    producto: str
    tienda: str
    is_premium: bool
    horizon_days: int
    prediction: float

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        if req.is_premium:
            pred = predict_price_premium(req.producto, req.tienda, req.horizon_days)
        else:
            pred = predict_price_free(req.producto, req.tienda, req.horizon_days)
        if pred is None:
            raise ValueError("No se obtuvo predicción")
        # Enviar notificación a Telegram sobre la predicción
        mensaje = (
            f"🔮 *Predicción de Precio*\n"
            f"• Producto: *{req.producto}*\n"
            f"• Tienda: *{req.tienda}*\n"
            f"• Premium: {'Sí' if req.is_premium else 'No'}\n"
            f"• Días al futuro: {req.horizon_days}\n"
            f"• Predicción: `$ {pred}`"
        )
        send_telegram(mensaje)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return PredictResponse(
        producto=req.producto,
        tienda=req.tienda,
        is_premium=req.is_premium,
        horizon_days=req.horizon_days,
        prediction=pred
    )
