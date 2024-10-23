from langchain_google_vertexai import ChatVertexAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage


class QuestionRefiner:
    def __init__(self, llm_client):
        self.llm_client = llm_client

class QuestionRefiner:
    def __init__(self, llm_client: ChatVertexAI):
        self.llm_client = llm_client

    def refine_question(self, user_input, relevant_turns):

        system_message_content = """
        Você é um especialista em reformular perguntas de conversas.

        Seu único objetivo é reformular a pergunta do usuário de forma clara e direta, sem fornecer respostas ou informações adicionais. 
        Diretrizes:
        a) Reformule a pergunta do usuário sem fornecer respostas diretas ou conteúdo adicional.
        b) Use as perguntas anteriores apenas para melhorar a clareza e a completude da pergunta.
        c) Certifique-se de que a pergunta reformulada seja sobre o que o usuário deseja saber, sem adicionar detalhes novos ou suposições.
        """

        formatted_messages = [SystemMessage(content=system_message_content)]


        for turn in relevant_turns:
            user_question = turn['input']
            assistant_response = turn['output']
            formatted_messages.append(HumanMessage(content=f"User: {user_question}"))
            formatted_messages.append(AIMessage(content=f"Assistant: {assistant_response}"))

        formatted_messages.append(HumanMessage(content=f"User: {user_input}"))

        reformulated_question = self.llm_client.invoke(formatted_messages).content

        return reformulated_question
