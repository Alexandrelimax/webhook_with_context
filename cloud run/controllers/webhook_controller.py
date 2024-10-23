from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any
from controllers.base_controller import BaseController
from repositories.search_history_conversation import SearchHistoryConversation
from services.conversational_assistant import ConversationalAssistant


class WebhookController(BaseController):
    def __init__(self, project_id: str, llm_client, retriever: Any):
        self.project_id = project_id
        self.llm_client = llm_client
        self.retriever = retriever


    def register_routes(self):
        self.router.add_api_route("/webhook", self.handle_webhook, methods=["POST"])


    async def handle_webhook(self, request_data: dict):
        try:
            user_input = request_data.get("text", "")
            session_id = request_data.get("session", "")

            conversation_history = SearchHistoryConversation(project_id=self.project_id, session_id=session_id)

            # Usa o ConversationalAssistant para processar a entrada e gerar a resposta
            conversational_assistant = ConversationalAssistant(self.llm_client, conversation_history, self.retriever)
            response_text = conversational_assistant.handle_user_input(user_input)

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
