
import json
import functions_framework
import os
import vertexai
from langchain_google_vertexai import ChatVertexAI

from repositories.search_history_conversation import SearchHistoryConversation
from services.conversational_assistant import ConversationalAssistant
from retrievers.structured_retriever import StructuredRetriever

# Importação dos defensores
from prompt_defender.layers.wall_defender import WallDefender
from prompt_defender.layers.keep_defender import KeepDefender
from prompt_defender.layers.drawbridge_defender import DrawbridgeDefender

# Importa dos decoradores
from decorators.handle_security_errors import handle_security_errors
from decorators.handle_general_errors import handle_general_errors

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

project_id = ""
region = "us-central1"
datastore_id = "ascensao_1729636149392"
location = 'global'

# Inicializa o Vertex AI com o project_id e a região
vertexai.init(project=project_id, location=region)

# Inicializa o cliente de LLM
llm_client = ChatVertexAI(
    model="gemini-1.5-flash-001",
    temperature=1,
    max_tokens=2000,
    max_retries=3,
    stop=None,
)

# Inicializa o retriever
structured_retriever = StructuredRetriever(project_id=project_id, location_id=location, data_store_id=datastore_id)

# Inicializa os defensores
wall_defender = WallDefender()
keep_defender = KeepDefender()
drawbridge_defender = DrawbridgeDefender(allow_unsafe_scripts=False)


@functions_framework.http
@handle_general_errors
@handle_security_errors
def webhook_function(request):
    # Recebe a entrada do usuário
    request_json = request.get_json()
    headers = {'Content-Type': 'application/json'}
    user_input = request_json.get("text", "")
    session_id = request_json.get("session", "")

    # 1. WallDefender: Sanitiza a entrada do usuário
    sanitized_input = wall_defender.sanitize_input(user_input)

    # 2. KeepDefender: Aplica defesas ao prompt
    protected_prompt = keep_defender.apply_defense(sanitized_input)

    # 3. ConversationalAssistant: Processa a entrada e gera a resposta
    conversation_history_handler = SearchHistoryConversation(project_id=project_id, session_id=session_id)
    conversational_assistant = ConversationalAssistant(llm_client, conversation_history_handler, structured_retriever)
    response_text = conversational_assistant.handle_user_input(protected_prompt)

    # 4. DrawbridgeDefender: Valida a resposta gerada pelo LLM
    validated_response = drawbridge_defender.validate_response(response_text)

    # Retorna a resposta final
    response = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [
                            validated_response
                        ]
                    }
                }
            ]
        }
    }
    return (response, 200, headers)
