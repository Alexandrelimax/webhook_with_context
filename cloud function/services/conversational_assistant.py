from langchain_google_vertexai import ChatVertexAI

from retrievers.base_retriever import BaseRetriever
from core.context_conversation import ContextConversation
from core.response_generator import ResponseGenerator
from repositories.search_history_conversation import SearchHistoryConversation


class ConversationalAssistant:

    def __init__(self, llm_client: ChatVertexAI, conversation_history_handler: SearchHistoryConversation, retriever: BaseRetriever):
        self.context_handler = ContextConversation(llm_client)
        self.response_handler = ResponseGenerator(llm_client)
        self.conversation_history_handler = conversation_history_handler
        self.retriever = retriever

    def handle_user_input(self, user_input: str) -> str:
        # Busca o histórico de conversas
        conversation_history = self.conversation_history_handler.get_last_turns()

        # Reformula a pergunta com base no histórico da conversa
        reformulated_question = self.context_handler.reformulate_question(user_input, conversation_history)

        # Busca os documentos mais relevantes usando o retriever
        search_results = self.retriever.search(reformulated_question)
        relevant_documents = [result["document"] for result in search_results]

        # Gera a resposta final com base no contexto e nos resultados da pesquisa
        response = self.response_handler.generate_response(user_input, conversation_history, relevant_documents)

        return response
