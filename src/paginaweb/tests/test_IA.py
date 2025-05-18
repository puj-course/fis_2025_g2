# tests/test_IA.py
import unittest
import numpy as np
import pandas as pd
import tempfile
import os
import sys
from unittest.mock import patch
from sklearn.multioutput import MultiOutputRegressor

# Configurar rutas para importar desde Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Backend.IA import (
    XGBoostStrategy, LinearRegressionStrategy, ContextoPrediccion,
    PredictionFacade, _find_column, _predict_for_tienda, save_predictions,
    PREDICTIONS_FILE, PredictionStrategy, load_data
)

# ===========================================
# Mocks actualizados con tiendas reales
# ===========================================
class TestData:
    @staticmethod
    def mock_load_data():
        dates = pd.date_range(start='2024-01-01', periods=5)
        return pd.DataFrame({
            'date': dates.repeat(3),
            'site': ['Exito', 'Olimpica', 'Jumbo'] * 5,
            'arroz 1kg': np.random.uniform(10000, 15000, 15),
            'azúcar 1kg': np.random.uniform(5000, 8000, 15),
            'aceite 3l': np.random.uniform(20000, 30000, 15)
        })

# ===========================================
# Todas las clases de prueba
# ===========================================
class TestPredictionPatterns(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.load_data_patcher = patch('Backend.IA.load_data', TestData.mock_load_data)
        cls.load_data_patcher.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.load_data_patcher.stop()
    
    def test_predicciones_tiendas_reales(self):
        """Prueba con nombres reales de tiendas (Exito/Olimpica/Jumbo)"""
        prediction = _predict_for_tienda('Exito', 1, 'premium')
        self.assertIn('arroz 1kg', prediction)
        self.assertTrue(10000 <= prediction['arroz 1kg'] <= 30000)

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        from Backend import IA
        self.original_path = IA.PREDICTIONS_FILE
        IA.PREDICTIONS_FILE = os.path.join(self.temp_dir.name, "pred_test.xlsx")
    
    def tearDown(self):
        from Backend import IA
        IA.PREDICTIONS_FILE = self.original_path
        self.temp_dir.cleanup()
    
    @patch('Backend.IA.load_data', TestData.mock_load_data)
    def test_guardado_predicciones(self):
        """Prueba que se genera el archivo Excel correctamente"""
        test_data = {
            'Exito': {'arroz 1kg': 15000.0},
            'Olimpica': {'azúcar 1kg': 7500.0}
        }
        
        save_predictions(test_data)
        expected_path = os.path.join(self.temp_dir.name, "pred_test.xlsx")
        self.assertTrue(os.path.exists(expected_path), f"Archivo {expected_path} no creado")

class TestAdvancedCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.real_data = TestData.mock_load_data()
        cls.load_data_patcher = patch('Backend.IA.load_data', TestData.mock_load_data)
        cls.load_data_patcher.start()
    
    @classmethod
    def tearDownClass(cls):
        cls.load_data_patcher.stop()
    
    def test_multiple_column_matches(self):
        """Prueba alias con múltiples coincidencias parciales"""
        df = self.real_data.copy()
        df['arroz premium 1kg'] = [15000] * 15
        result = _find_column(df, 'arroz')
        self.assertEqual(result, 'arroz 1kg')
    
    def test_premium_vs_free_difference(self):
        """Prueba diferencia entre modelos premium y free"""
        facade = PredictionFacade()
        premium = facade.get_prediction('arroz 1kg', 'Exito', 7, True)
        free = facade.get_prediction('arroz 1kg', 'Exito', 7, False)
        self.assertNotEqual(premium, free)
    
    def test_historical_data_influence(self):
        """Prueba influencia de datos históricos"""
        pred1 = _predict_for_tienda('Exito', 1, 'premium')
        modified_data = self.real_data.copy()
        modified_data['arroz 1kg'] *= 1.2
        
        with patch('Backend.IA.load_data', return_value=modified_data):
            pred2 = _predict_for_tienda('Exito', 1, 'premium')
        
        self.assertNotAlmostEqual(pred1['arroz 1kg'], pred2['arroz 1kg'], delta=1000)
    
    def test_invalid_horizon_days(self):
        """Prueba días de predicción inválidos"""
        with self.assertRaises(ValueError):
            _predict_for_tienda('Exito', -5, 'premium')
        with self.assertRaises(ValueError):
            _predict_for_tienda('Exito', 'cinco', 'free')
    
    def test_strategy_interface(self):
        """Prueba implementación de interfaz Strategy"""
        class InvalidStrategy(PredictionStrategy): pass
        
        with self.assertRaises(TypeError):
            ContextoPrediccion(InvalidStrategy())
    
    def test_empty_store_data(self):
        """Prueba tiendas sin datos históricos"""
        with patch('Backend.IA.load_data') as mock_load:
            mock_load.return_value = pd.DataFrame(columns=['date', 'site', 'arroz 1kg'])
            with self.assertRaises(ValueError):
                _predict_for_tienda('NuevaTienda', 1, 'premium')
    
    def test_facade_error_handling(self):
        """Prueba manejo de errores en fachada"""
        with self.assertRaises(KeyError):
            PredictionFacade().get_prediction('producto_inexistente', 'Exito', 1, True)
    
    def test_data_cache_singleton(self):
        """Prueba comportamiento singleton del cache"""
        data1 = load_data()
        data2 = load_data()
        self.assertIs(data1, data2)
        
        with patch('Backend.IA._df_cache', None):
            data3 = load_data()
            self.assertIsNot(data1, data3)

# ===========================================
# Ejecución principal
# ===========================================
if __name__ == '__main__':
    unittest.main(verbosity=2)