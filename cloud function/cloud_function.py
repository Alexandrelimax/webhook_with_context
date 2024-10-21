import json
import functions_framework

from langchain_google_vertexai import ChatVertexAI

from repositories.search_history_conversation import SearchHistoryConversation
from services.conversational_assistant import ConversationalAssistant
from retrievers.structured_retriever import StructuredRetriever


project_id = "meu_projeto"
region = "us-central1"
datastore_id = "3541312121684351asd"
llm_client = ChatVertexAI(model="gemini-1.5-flash-001", temperature=0)
structured_retriever = StructuredRetriever(project_id=project_id, location_id=region, data_store_id=datastore_id)

@functions_framework.http
def webhook_function(request):
    try:

        request_json = request.get_json()
        headers = {'Content-Type': 'application/json'}

        user_input = request_json.get("text", "")
        session_id = request_json.get("session", "")


        conversation_history_handler = SearchHistoryConversation(project_id=project_id, session_id=session_id)

        # Usa o ConversationalAssistant para processar a entrada e gerar a resposta
        conversational_assistant = ConversationalAssistant(llm_client, conversation_history_handler, structured_retriever)
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
        return (response, 200, headers)

    except Exception as e:
        print(f"Erro ao processar a requisição: {e}")
        return {"error": str(e)}, 500
