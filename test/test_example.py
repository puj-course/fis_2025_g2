import unittest
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta

class TestModeloPrediccion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cargar datos de ejemplo
        cls.archivo = "precios.xlsx"
        cls.df = pd.read_excel(cls.archivo)
        cls.df['Date'] = pd.to_datetime(cls.df['Date'])

        # Preparar datos para prueba
        cls.tienda = cls.df['Site'].unique()[0]
        cls.producto = cls.df.columns[2]  # Primer producto
        cls.datos_tienda = cls.df[cls.df['Site'] == cls.tienda].sort_values("Date")
        cls.datos_tienda["Días"] = (cls.datos_tienda["Date"] - cls.datos_tienda["Date"].min()).dt.days

    def test_formato_fecha(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df['Date']), "La columna 'Date' debe ser datetime")

    def test_columnas_existentes(self):
        columnas_esperadas = ['Date', 'Site']
        for col in columnas_esperadas:
            self.assertIn(col, self.df.columns)

    def test_entrenamiento_modelo(self):
        X = self.datos_tienda[["Días"]]
        y = self.datos_tienda[self.producto]
        modelo = LinearRegression()
        modelo.fit(X, y)
        self.assertIsNotNone(modelo.coef_, "El modelo debe tener coeficientes después de entrenar")

    def test_prediccion_valida(self):
        X = self.datos_tienda[["Días"]]
        y = self.datos_tienda[self.producto]
        modelo = LinearRegression()
        modelo.fit(X, y)
        pred_día = (self.df['Date'].max() + timedelta(days=1) - self.datos_tienda["Date"].min()).days
        pred = modelo.predict([[pred_día]])[0]
        self.assertIsInstance(pred, float, "La predicción debe ser un número flotante")

if __name__ == '__main__':
    unittest.main()
