from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class WebhookController(BaseController):
    def __init__(self, chat_bot_service, intent_handler):
        self.chat_bot_service = chat_bot_service
        self.intent_handler = intent_handler
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/webhook", self.handle_webhook, methods=["POST"])

    async def handle_webhook(self, request_data: dict):
        try:
            # Processar a requisição do Dialogflow
            user_input = request_data.get("text", "")
            response_text = await self.chat_bot_service.process_text(user_input)

            # Formatar a resposta conforme o padrão
            response = {
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": [
                                    response_text
                                ]
                            }
                        }
                    ]
                }
            }
            return JSONResponse(content=response)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
