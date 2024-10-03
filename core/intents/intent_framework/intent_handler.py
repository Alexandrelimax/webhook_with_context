from core.context.memory_manager import MemoryManager
from .handler_config import configure_handlers
from app.interfaces.intent_handler_interface import IntentHandlerInterface
from typing import  Dict, Union


class IntentHandler:
    
    def __init__(self, memory_manager: MemoryManager):
        # O MemoryManager é responsável por gerenciar a memória de cada sessão
        self.memory_manager = memory_manager
        self.factory = configure_handlers()

    def handle(self, intent_name: str, fulfillment_text: str, session_id: str) -> dict:
        # Pega a memória específica da sessão
        memory = self.memory_manager.get_memory(session_id)
        
        # Verifica fulfilments simples
        simple_fulfillment = self._get_simple_fulfillment(intent_name)

        if simple_fulfillment:
            memory.add_message(role="system", message=simple_fulfillment)
            return {"message": simple_fulfillment}
        
        # Processa intenções complexas
        handler_class = self.factory.get_handler(intent_name)
        if handler_class:
            handler = handler_class(memory)
            return handler.handle(fulfillment_text)
        
        return {"message": "Intenção não reconhecida."}

    def _get_simple_fulfillment(self, intent_name: str) -> Union[str, None]:
        simple_fulfillments = {
            'greeting': 'Olá! Como posso ajudar você hoje?',
            'goodbye': 'Até logo! Tenha um ótimo dia!',
        }
        return simple_fulfillments.get(intent_name)
