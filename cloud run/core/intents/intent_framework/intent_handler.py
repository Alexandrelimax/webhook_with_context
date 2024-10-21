from core.context.conversation_buffer_memory import MemoryManager
from .handler_config import configure_handlers
from app.interfaces.intent_handler_interface import IntentHandlerInterface
from typing import Union

class IntentHandler:
    def __init__(self, memory_manager: MemoryManager):
        # O MemoryManager é responsável por gerenciar a memória de cada sessão
        self.memory_manager = memory_manager
        self.factory = configure_handlers()

    def handle(self, intent_name: str, user_message: str, session_id: str) -> dict:
        # Pega a memória específica da sessão
        memory = self.memory_manager.get_memory(session_id)
        
        # Adiciona a nova interação do usuário
        memory.add_message(role="user", message=user_message)

        # Processa intenções complexas
        handler_class = self.factory.get_handler(intent_name)
        if handler_class:
            handler = handler_class(memory)
            response = handler.handle(user_message)
        else:
            response = "Intenção não reconhecida."

        # Adiciona a resposta do chatbot à memória
        memory.add_message(role="assistant", message=response)

        # Salva a nova interação no Redis
        self.memory_manager.redis_repository.save_interaction(session_id, user_message, response)

        return {"message": response}
