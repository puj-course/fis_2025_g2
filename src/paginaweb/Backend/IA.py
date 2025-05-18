import pandas as pd
import numpy as np
import os
from datetime import timedelta
from abc import ABC, abstractmethod
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression

# === PATRÓN STRATEGY IMPLEMENTACIÓN ===
class PredictionStrategy(ABC):
    @abstractmethod
    def train_model(self, X, y):
        raise NotImplementedError("Método abstracto debe ser implementado")

class XGBoostStrategy(PredictionStrategy):
    def train_model(self, X, y):
        base = XGBRegressor(
            n_estimators=200, 
            max_depth=5, 
            learning_rate=0.1,
            objective='reg:squarederror', 
            random_state=42
        )
        model = MultiOutputRegressor(base)
        return model.fit(X, y)

class LinearRegressionStrategy(PredictionStrategy):
    def train_model(self, X, y):
        model = MultiOutputRegressor(LinearRegression())
        return model.fit(X, y)

class ContextoPrediccion:
    def __init__(self, strategy: PredictionStrategy):
        self._strategy = strategy
    
    def ejecutar_entrenamiento(self, X, y):
        return self._strategy.train_model(X, y)
# === FIN PATRÓN STRATEGY ===

# --- Configuración general ---
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "precios.xlsx")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "predicciones.xlsx")

# Cache de datos usando singleton implícito
_df_cache = None

def load_data():
    global _df_cache
    if _df_cache is None:
        df = pd.read_excel(DATA_FILE)
        df.columns = [col.lower() if isinstance(col, str) else col for col in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        _df_cache = df
    return _df_cache

def _find_column(df, alias):
    alias = alias.lower()
    cols = [c for c in df.columns if alias in c]
    if not cols:
        raise KeyError(f"Alias de producto desconocido: '{alias}'")
    cols_sorted = sorted(cols, key=lambda x: len(x))
    return cols_sorted[0]

def _train_model(df_tienda, model_type='premium'):
    fecha_inicio = df_tienda['date'].min()
    dias = ((df_tienda['date'] - fecha_inicio).dt.days).values.reshape(-1, 1)
    productos = df_tienda.columns.drop(['date', 'site'])
    X, y = dias, df_tienda[productos]

    if model_type == 'premium':
        estrategia = XGBoostStrategy()
    else:
        estrategia = LinearRegressionStrategy()
    
    contexto = ContextoPrediccion(estrategia)
    modelo = contexto.ejecutar_entrenamiento(X, y)
    
    return modelo, list(productos), fecha_inicio

def _predict_for_tienda(tienda, days_ahead, model_type):
    # Validación de días de predicción
    if not isinstance(days_ahead, int) or days_ahead < 1:
        raise ValueError("horizon_days debe ser un entero positivo")
    
    df = load_data()
    datos = df[df['site'].str.lower() == tienda.lower()].sort_values('date')
    
    if datos.empty:
        raise ValueError(f"No hay datos para la tienda '{tienda}'")

    modelo, productos, fecha_inicio = _train_model(datos, model_type)
    last_day = datos['date'].max()
    days_since_start = (last_day - fecha_inicio).days
    dia_pred = np.array([[days_since_start + days_ahead]])
    pred_vals = modelo.predict(dia_pred)[0]
    return dict(zip(productos, np.round(pred_vals, 2)))

def predict_price_premium(alias, tienda, horizon_days=1):
    df = load_data()
    col = _find_column(df, alias)
    preds = _predict_for_tienda(tienda, horizon_days, model_type='premium')
    return preds.get(col)

def predict_price_free(alias, tienda, horizon_days=1):
    df = load_data()
    col = _find_column(df, alias)
    preds = _predict_for_tienda(tienda, horizon_days, model_type='free')
    return preds.get(col)

def save_predictions(preds_by_tienda, days_ahead=1):
    global PREDICTIONS_FILE  # Usar variable global actualizada
    df = load_data()
    manana = df['date'].max() + timedelta(days=days_ahead)
    rows = []
    
    for tienda, pred in preds_by_tienda.items():
        for producto, val in pred.items():
            rows.append({
                'date': manana,
                'site': tienda,
                'producto': producto,
                'prediccion': val
            })
    
    out_df = pd.DataFrame(rows)
    
    if os.path.exists(PREDICTIONS_FILE):
        prev = pd.read_excel(PREDICTIONS_FILE)
        out_df = pd.concat([prev, out_df], ignore_index=True)
    
    out_df.to_excel(PREDICTIONS_FILE, index=False)
    return out_df

# === PATRÓN FACADE ===
class PredictionFacade:
    def get_prediction(self, alias, tienda, horizon_days, premium=False):
        if not isinstance(horizon_days, int) or horizon_days < 1:
            raise ValueError("El horizonte de días debe ser un entero positivo")
        
        if premium:
            return predict_price_premium(alias, tienda, horizon_days)
        return predict_price_free(alias, tienda, horizon_days)

# === Función de prueba ===
def test():
    df = load_data()
    print("Columnas disponibles:", df.columns.tolist())
    tiendas = df['site'].unique()
    productos = [c for c in df.columns if c not in ('date', 'site')]
    
    facade = PredictionFacade()
    for alias in productos:
        print(f"\n--- {alias} ---")
        print("Premium:", facade.get_prediction(alias, "Olimpica", 1, True))
        print("Free:", facade.get_prediction(alias, "Olimpica", 1, False))

if __name__ == '__main__':
    test()