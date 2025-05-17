import pandas as pd
import numpy as np
import os
from datetime import timedelta
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import LinearRegression

# --- Configuración general ---
BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "precios.xlsx")
PREDICTIONS_FILE = os.path.join(BASE_DIR, "predicciones.xlsx")

# Cargar y preparar datos
_df_cache = None

def load_data():
    global _df_cache
    if _df_cache is None:
        df = pd.read_excel(DATA_FILE)
        df.columns = [col.lower() if isinstance(col, str) else col for col in df.columns]
        df['date'] = pd.to_datetime(df['date'])
        _df_cache = df
    return _df_cache

# Ayuda a mapear alias a columnas basadas en coincidencia parcial
def _find_column(df, alias):
    alias = alias.lower()
    cols = [c for c in df.columns if alias in c]
    if not cols:
        raise KeyError(f"Alias de producto desconocido: '{alias}'")
    # si hay múltiples coincidencias, elige la más corta o exacta
    cols_sorted = sorted(cols, key=lambda x: len(x))
    return cols_sorted[0]

# Entrena un modelo (premium = XGBoost, free = lineal)
def _train_model(df_tienda, model_type='premium'):
    fecha_inicio = df_tienda['date'].min()
    dias = ((df_tienda['date'] - fecha_inicio).dt.days).values.reshape(-1, 1)
    productos = df_tienda.columns.drop(['date', 'site'])
    X, y = dias, df_tienda[productos]

    if model_type == 'premium':
        base = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1,
                            objective='reg:squarederror', random_state=42)
        model = MultiOutputRegressor(base)
    else:
        model = MultiOutputRegressor(LinearRegression())

    model.fit(X, y)
    return model, list(productos), fecha_inicio

# Predicción general para una tienda
def _predict_for_tienda(tienda, days_ahead, model_type):
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

# Funciones para obtener predicciones individuales (alias flexible)
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

# Guardar predicciones en Excel
def save_predictions(preds_by_tienda, days_ahead=1):
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

# Ejemplo de uso
def test():
    df = load_data()
    print("Columnas disponibles:", df.columns.tolist())
    tiendas = df['site'].unique()
    productos = [c for c in df.columns if c not in ('date', 'site')]
    for alias in productos:
        print(f"--- {alias} ---")
        print("Premium:", {t: predict_price_premium(alias, t) for t in tiendas})
        print("Free:", {t: predict_price_free(alias, t) for t in tiendas})

if __name__ == '__main__':
    test()
