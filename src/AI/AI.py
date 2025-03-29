import pandas as pd

# Cargar el archivo Excel
ruta_archivo = r'C:\Users\romer\Downloads\IPC Variación.xlsx'
df = pd.read_excel(ruta_archivo, skiprows=6)  


df.columns = df.iloc[0]  
df = df[1:]  


df.rename(columns={df.columns[0]: "Mes"}, inplace=True)


df.reset_index(drop=True, inplace=True)


print(df.head())


