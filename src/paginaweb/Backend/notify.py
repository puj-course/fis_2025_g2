# Backend/notify.py
import requests
from abc import ABC, abstractmethod

# ===== PATRÓN STRATEGY =====
class NotificationStrategy(ABC):
    """Interfaz común para todas las estrategias de notificación"""
    @abstractmethod
    def send(self, message: str) -> bool:
        pass

class TelegramStrategy(NotificationStrategy):
    """Estrategia concreta para notificaciones via Telegram"""
    def __init__(self, token: str, chat_id: str):
        self._token = token
        self._chat_id = chat_id
        self._base_url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        
    def send(self, message: str) -> bool:
        payload = {
            "chat_id": self._chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self._base_url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error Telegram: {e}")
            return False

# ===== PATRÓN SINGLETON =====
class NotificationManager:
    """Singleton para gestionar el servicio de notificaciones"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Configuración inicial (valores por defecto)
            cls._instance._strategy = None
            cls._instance._token = "7200520916:AAFB9qSZZd0-mGWpbU-lq2MU9bb_JKD3E2o"
            cls._instance._chat_id = "7326632476"
        return cls._instance
    
    def setup_telegram(self):
        """Configurar estrategia Telegram usando valores singleton"""
        self._strategy = TelegramStrategy(self._token, self._chat_id)
        
    def send_notification(self, message: str) -> bool:
        """Método principal de notificación"""
        if self._strategy:
            return self._strategy.send(message)
        raise RuntimeError("Estrategia de notificación no configurada")

# ===== PATRÓN DECORATOR =====
class NotificationDecorator(NotificationStrategy):
    """Decorator base para funcionalidades adicionales"""
    def __init__(self, wrappee: NotificationStrategy):
        self._wrappee = wrappee
        
    def send(self, message: str) -> bool:
        return self._wrappee.send(message)

class LoggingDecorator(NotificationDecorator):
    """Decorator para agregar logging"""
    def send(self, message: str) -> bool:
        print(f"Enviando mensaje: {message[:30]}...")  # Log parcial
        result = super().send(message)
        print(f"Resultado envío: {'Éxito' if result else 'Falló'}")
        return result

class ValidationDecorator(NotificationDecorator):
    """Decorator para validar mensajes"""
    def send(self, message: str) -> bool:
        if len(message) > 4096:
            print("Error: Mensaje demasiado largo para Telegram")
            return False
        return super().send(message)

# ==== FACHADA PARA USO SIMPLIFICADO ====
def send_telegram(message: str):
    """Fachada para compatibilidad con código existente"""
    manager = NotificationManager()
    if not manager._strategy:
        manager.setup_telegram()
        
    # Cadena de decoradores
    notifier = ValidationDecorator(
        LoggingDecorator(
            manager._strategy
        )
    )
    
    return notifier.send(message)