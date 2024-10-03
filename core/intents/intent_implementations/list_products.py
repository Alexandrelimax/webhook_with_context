from app.interfaces.intent_handler_interface import IntentHandlerInterface
from core.context.conversation_buffer_memory import BufferMemory

class ProductsHandler(IntentHandlerInterface):
    def __init__(self, memory: BufferMemory):
        self.memory = memory

    def handle(self, fulfillment_text: str) -> dict:
        # Recupera informações do contexto, caso existam
        category = self.memory.get("product_category", None)

        # Se o fulfillment_text especificar uma categoria, atualiza o contexto
        if fulfillment_text:
            self.memory.set("product_category", fulfillment_text)
            category = fulfillment_text

        # Simulando a lógica de obtenção de produtos com base na categoria
        products = self.get_products_by_category(category)
        
        # Retorna os produtos ou uma mensagem default
        if products:
            return {
                "message": f"Here are the products for the category '{category}':",
                "products": products
            }
        else:
            return {"message": "No products available for the specified category."}

    def get_products_by_category(self, category: str) -> list:
        # Simulação de produtos. Idealmente, aqui você teria uma chamada para um serviço ou banco de dados.
        all_products = {
            "car": ["Car Product 1", "Car Product 2", "Car Product 3"],
            "agriculture": ["Agriculture Product 1", "Agriculture Product 2"],
            "default": ["General Product 1", "General Product 2"]
        }
        
        # Retorna produtos com base na categoria, se disponível
        return all_products.get(category.lower(), all_products["default"])
