import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from datetime import timedelta

# 1. Cargar datos
archivo = "precios.xlsx"  # tu archivo principal
df = pd.read_excel(archivo)

# Asegúrate de que la fecha esté en formato datetime
df['Date'] = pd.to_datetime(df['Date'])

# 2. Variables
productos = df.columns[2:]  # Ignorar Date y Site
tiendas = df['Site'].unique()
predicciones_path = "predicciones.xlsx"

# 3. Entrenar modelo y predecir
hoy = df['Date'].max()
mañana = hoy + timedelta(days=1)
nuevas_predicciones = []

for tienda in tiendas:
    datos_tienda = df[df['Site'] == tienda].sort_values("Date")
    datos_tienda["Días"] = (datos_tienda["Date"] - datos_tienda["Date"].min()).dt.days

    for producto in productos:
        X = datos_tienda[["Días"]]
        y = datos_tienda[producto]

        modelo = LinearRegression()
        modelo.fit(X, y)

        pred_día = (mañana - datos_tienda["Date"].min()).days
        prediccion = modelo.predict([[pred_día]])[0]

        nuevas_predicciones.append({
            "Date": mañana,
            "Site": tienda,
            "Producto": producto,
            "Predicción": round(prediccion, 2)
        })

# 4. Guardar predicciones
pred_df = pd.DataFrame(nuevas_predicciones)

if os.path.exists(predicciones_path):
    pred_guardadas = pd.read_excel(predicciones_path)
    pred_df = pd.concat([pred_guardadas, pred_df], ignore_index=True)

pred_df.to_excel(predicciones_path, index=False)
print(f"✅ Predicciones guardadas en {predicciones_path}")

# 5. BONUS: Evaluar si ya existen precios reales
comparaciones = []
for row in nuevas_predicciones:
    real = df[(df['Date'] == row['Date']) & (df['Site'] == row['Site'])]
    if not real.empty:
        real_valor = real[row['Producto']].values[0]
        error = abs(real_valor - row["Predicción"]) / real_valor
        comparaciones.append({
            "Producto": row["Producto"],
            "Tienda": row["Site"],
            "Predicción": row["Predicción"],
            "Real": real_valor,
            "Error relativo": round(error, 3)
        })

if comparaciones:
    comp_df = pd.DataFrame(comparaciones)
    print("📊 Comparación de predicciones vs valores reales:")
    print(comp_df)
