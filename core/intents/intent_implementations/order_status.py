from app.interfaces.intent_handler_interface import IntentHandlerInterface
from core.context.conversation_buffer_memory import BufferMemory

class OrderStatusHandler(IntentHandlerInterface):
    
    def __init__(self, memory: BufferMemory):
        self.memory = memory

    def handle(self, fulfillment_text: str) -> dict:
        # Verifica se já existe um número de pedido no contexto
        order_id = self.memory.get("order_id")

        if not order_id:
            # Se não houver ID do pedido, assume que fulfillment_text contém o ID
            self.memory.set("order_id", fulfillment_text)
            return {"message": "Número do pedido registrado. Consultando o status..."}

        # Se já houver um número de pedido no contexto, continua o processo
        status = self.check_order_status(order_id)
        return {"message": f"O status do seu pedido {order_id} é: {status}"}
    
    def check_order_status(self, order_id: str) -> str:
        # Simulação da lógica de checagem do status do pedido
        return "Em trânsito"
