

import pandas as pd

# Cargar el archivo Excel
ruta_archivo = r'C:\Users\romer\Downloads\IPC Variación.xlsx'
df = pd.read_excel(ruta_archivo, skiprows=5)  


df.columns = df.iloc[0]  
df = df[1:]  


df.rename(columns={df.columns[0]: "Mes"}, inplace=True)


df.reset_index(drop=True, inplace=True)



print(df.head())

df_long = df.melt(id_vars=["Mes"], var_name="Año", value_name="IPC")

# Convertir "Año" a tipo numérico
df_long["Año"] = pd.to_numeric(df_long["Año"])

# Ordenar por año y mes
df_long = df_long.sort_values(by=["Año", "Mes"])

# Mostrar los primeros datos transformados
print(df_long.head())


meses_validos = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Filtrar solo las filas que contienen meses válidos
df_long = df_long[df_long["Mes"].isin(meses_validos)]

# Reiniciar índices
df_long.reset_index(drop=True, inplace=True)

# Mostrar los primeros datos limpios
print(df_long.head())

print(df_long["Año"].unique())  # Ver los años presentes en el DataFrame
print(df_long["Mes"].unique())  # Ver los meses presentes

# Ordenar por año y mes
df_long["Año"] = df_long["Año"].astype(int)  # Convertir a entero si es necesario
df_long["Mes"] = pd.Categorical(
    df_long["Mes"],
    categories=[
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ],
    ordered=True
)
df_long = df_long.sort_values(by=["Año", "Mes"]).reset_index(drop=True)

print(df_long.head(15))  # Mostrar las primeras 15 filas ordenadas
