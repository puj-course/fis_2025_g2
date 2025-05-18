// backend/telegramNotifier.js

// ===== PATRÓN SINGLETON =====
class TelegramService {
    constructor() {
        if (!TelegramService.instance) {
            this._TOKEN = "7200520916:AAFB9qSZZd0-mGWpbU-lq2MU9bb_JKD3E2o";
            this._CHAT_ID = "7326632476";
            this._BASE_URL = `https://api.telegram.org/bot${this._TOKEN}/sendMessage`;
            TelegramService.instance = this;
        }
        return TelegramService.instance;
    }

    // ===== PATRÓN STRATEGY =====
    setSenderStrategy(strategy) {
        this._sendStrategy = strategy;
    }

    async send(message) {
        if (!this._sendStrategy) {
            throw new Error("Estrategia de envío no configurada");
        }
        return this._sendStrategy.send(message);
    }
}

// Estrategia base
class SendStrategy {
    constructor(service) {
        this.service = service;
    }

    async send(message) {
        throw new Error("Método abstracto debe ser implementado");
    }
}

// Estrategia concreta para Telegram
class TelegramStrategy extends SendStrategy {
    async send(message) {
        try {
            const response = await fetch(this.service._BASE_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    chat_id: this.service._CHAT_ID,
                    text: message
                })
            });
            
            const data = await response.json();
            return data.ok;
        } catch (error) {
            console.error("Error en envío:", error);
            return false;
        }
    }
}

// ===== PATRÓN DECORATOR =====
class NotificationDecorator {
    constructor(notifier) {
        this.notifier = notifier;
    }

    async send(message) {
        return this.notifier.send(message);
    }
}

// Decorator concreto para logging
class LoggingDecorator extends NotificationDecorator {
    async send(message) {
        console.log(`Intentando enviar mensaje: ${message.substring(0, 15)}...`);
        const result = await super.send(message);
        console.log(`Resultado del envío: ${result ? "Éxito" : "Falló"}`);
        return result;
    }
}

// Decorator concreto para validación
class ValidationDecorator extends NotificationDecorator {
    async send(message) {
        if (message.length > 4096) {
            console.error("Mensaje excede límite de Telegram");
            return false;
        }
        return super.send(message);
    }
}

// ===== FACHADA Y MÓDULO EXPORTADO =====
const telegramService = new TelegramService();
telegramService.setSenderStrategy(new TelegramStrategy(telegramService));

// Versión decorada por defecto
const decoratedService = new ValidationDecorator(
    new LoggingDecorator(
        telegramService._sendStrategy
    )
);

// Compatibilidad con implementación anterior
async function sendTelegramMessage(message) {
    return decoratedService.send(message);
}

module.exports = {
    TelegramService,
    sendTelegramMessage
};