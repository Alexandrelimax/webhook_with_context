# core/intents/handler_factory.py

from typing import Dict, Type
from app.interfaces.intent_handler_interface import IntentHandlerInterface

class HandlerFactory:
    
    def __init__(self):
        self._handlers: Dict[str, Type[IntentHandlerInterface]] = {}

    def register_handler(self, intent_name: str, handler_class: Type[IntentHandlerInterface]):
        """Registra um manipulador de intenção com um nome específico."""
        self._handlers[intent_name] = handler_class

    def get_handler(self, intent_name: str) -> Type[IntentHandlerInterface]:
        """Retorna o manipulador correspondente ao nome da intenção fornecida."""
        return self._handlers.get(intent_name)
