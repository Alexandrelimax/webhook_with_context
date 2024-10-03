from fastapi import FastAPI
from intent_handler import IntentHandler
from core.context.conversation_buffer_memory import MemoryManager
from webhook_controller import WebhookController

app = FastAPI()

# Inicializa o MemoryManager e o IntentHandler
memory_manager = MemoryManager()
intent_handler = IntentHandler(memory_manager)

# Cria uma instância do WebhookController
webhook_controller = WebhookController(intent_handler)

# Inclui o router do WebhookController
app.include_router(webhook_controller.router)

@app.get("/")
def read_root():
    return {"message": "Teste API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
