from langchain_google_vertexai import ChatVertexAI
from langchain_core.documents import Document  # Certifique-se de importar o tipo Document


class ResponseGenerator:
    """Classe responsável por gerar uma resposta conversacional com base nos resultados da pesquisa e no contexto."""

    def __init__(self, llm_client: ChatVertexAI):
        self.llm_client = llm_client

    def generate_response(self, user_input: str, conversation_history: list, relevant_documents: list[Document]) -> str:
        # Instruções para gerar uma resposta natural e fluida
        prompt_instructions = """
        Você é um assistente inteligente que responde com base no contexto da conversa anterior e nos resultados da pesquisa.

        Seu objetivo é:
        a) Responder de forma clara e completa, utilizando os resultados da pesquisa.
        b) Manter o tom conversacional, fluido e natural, sincronizado com o estilo da conversa anterior.
        c) Se possível, conectar a resposta ao que foi discutido anteriormente.
        d) Utilizar os resultados da pesquisa para fornecer informações úteis, mencionando os documentos relevantes quando aplicável.
        """

        formatted_history = [("system", prompt_instructions)]

        if conversation_history:
            for user_question, bot_answer in conversation_history:
                formatted_history.append(("human", user_question))
                formatted_history.append(("system", bot_answer))

        # Adiciona a nova pergunta do usuário
        formatted_history.append(("human", user_input))

        # Adiciona os resultados relevantes da pesquisa como contexto para a LLM
        search_context = "\n\n".join([f"Documento: {doc.metadata.get('title', 'Sem título')}\n"
                                      f"Conteúdo: {doc.page_content}" for doc in relevant_documents])
        
        formatted_history.append(("system", f"Resultados da pesquisa:\n{search_context}"))

        # Invoca a LLM para gerar a resposta conversacional
        conversational_answer = self.llm_client.invoke(formatted_history).content

        return conversational_answer

