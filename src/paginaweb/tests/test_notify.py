# tests/test_notify.py
import unittest
from unittest.mock import patch, MagicMock
from Backend.notify import (
    NotificationStrategy,
    TelegramStrategy,
    NotificationManager,
    NotificationDecorator,
    LoggingDecorator,
    ValidationDecorator,
    send_telegram
)

class TestTelegramStrategy(unittest.TestCase):
    @patch('requests.post')
    def test_send_success(self, mock_post):
        """Prueba envío exitoso a Telegram"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        strategy = TelegramStrategy("fake_token", "fake_chat")
        result = strategy.send("Mensaje de prueba")
        
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_send_failure(self, mock_post):
        """Prueba fallo en el envío a Telegram"""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        strategy = TelegramStrategy("fake_token", "fake_chat")
        result = strategy.send("Mensaje de prueba")
        
        self.assertFalse(result)
    
    @patch('requests.post')
    def test_send_exception(self, mock_post):
        """Prueba manejo de excepciones"""
        mock_post.side_effect = Exception("Error de conexión")
        
        strategy = TelegramStrategy("fake_token", "fake_chat")
        result = strategy.send("Mensaje de prueba")
        
        self.assertFalse(result)

class TestNotificationManager(unittest.TestCase):
    def test_singleton_pattern(self):
        """Prueba que el patrón Singleton funciona correctamente"""
        manager1 = NotificationManager()
        manager2 = NotificationManager()
        self.assertIs(manager1, manager2)
    
    def test_notification_flow(self):
        """Prueba configuración y envío de notificación"""
        manager = NotificationManager()
        manager.setup_telegram()
        
        with patch.object(manager._strategy, 'send') as mock_send:
            mock_send.return_value = True
            result = manager.send_notification("Test")
            
            self.assertTrue(result)
            mock_send.assert_called_once_with("Test")
    
    def test_unconfigured_strategy(self):
        """Prueba error cuando no hay estrategia configurada"""
        manager = NotificationManager()
        manager._strategy = None  # Reset para prueba
        
        with self.assertRaises(RuntimeError):
            manager.send_notification("Mensaje")

class TestDecorators(unittest.TestCase):
    def test_validation_decorator(self):
        """Prueba validación de longitud de mensaje"""
        mock_strategy = MagicMock()
        decorator = ValidationDecorator(mock_strategy)
        
        # Mensaje demasiado largo
        result = decorator.send("X" * 4097)
        self.assertFalse(result)
        
        # Mensaje válido
        result = decorator.send("Mensaje válido")
        self.assertTrue(mock_strategy.send.called)
    
    @patch('builtins.print')
    def test_logging_decorator(self, mock_print):
        """Prueba logging de operaciones"""
        mock_strategy = MagicMock()
        mock_strategy.send.return_value = True
        decorator = LoggingDecorator(mock_strategy)
        
        result = decorator.send("Mensaje de prueba")
        
        self.assertTrue(result)
        mock_print.assert_any_call("Enviando mensaje: Mensaje de prueba...")
        mock_print.assert_any_call("Resultado envío: Éxito")

class TestIntegration(unittest.TestCase):
    @patch('requests.post')
    @patch('builtins.print')
    def test_full_flow(self, mock_print, mock_post):
        """Prueba integración completa con decoradores"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Prueba mensaje válido
        result = send_telegram("Mensaje válido")
        self.assertTrue(result)
        
        # Prueba mensaje demasiado largo
        result = send_telegram("X" * 4097)
        self.assertFalse(result)
        mock_print.assert_any_call("Error: Mensaje demasiado largo para Telegram")

if __name__ == '__main__':
    unittest.main(verbosity=2)