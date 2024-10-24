from langchain_google_vertexai import ChatVertexAI
from langchain.schema import SystemMessage, HumanMessage

class ContextConversation:
    def __init__(self, llm_client: ChatVertexAI):
        self.llm_client = llm_client

    def reformulate_question(self, user_input: str, conversation_history: list) -> str:

        prompt_instructions = """
        Você é um especialista em reformular perguntas de conversas.

        Seu único objetivo é reformular a pergunta do usuário de forma clara e direta, sem fornecer respostas ou informações adicionais. Apenas transforme a pergunta para torná-la mais completa, utilizando apenas as perguntas anteriores do usuário como contexto.

        Diretrizes:
        a) Reformule a pergunta do usuário sem fornecer respostas diretas ou conteúdo adicional.
        b) Use as perguntas anteriores apenas para melhorar a clareza e a completude da pergunta, sem criar novas informações ou suposições.
        c) Certifique-se de que a pergunta reformulada seja sobre o que o usuário deseja saber, sem adicionar detalhes novos ou suposições.
        d) Não forneça conselhos, recomendações ou respostas como parte da reformulação.
        e) Caso não haja histórico de perguntas, trate a pergunta como uma nova interação.

        Exemplos de perguntas reformuladas:
        Exemplo 1:
        Histórico de perguntas:
        Usuário: Quem é o presidente do Brasil?

        Pergunta do usuário: E da Argentina?
        Pergunta reformulada: Quem é o presidente da Argentina?

        Exemplo 2:
        Histórico de perguntas:
        Usuário: Qual é a capital do Japão?

        Pergunta do usuário: Qual a cidade mais populosa?
        Pergunta reformulada: Qual é a cidade mais populosa do Japão?

        Exemplo 3:
        Histórico de perguntas:
        Usuário: Como funciona o sistema de pontos da empresa?

        Pergunta do usuário: E como eu uso esses pontos?
        Pergunta reformulada: Como posso usar os pontos acumulados no sistema da empresa?

        Exemplo 4:
        Histórico de perguntas:
        Usuário: Quais são as principais políticas do Presidente Lula?

        Pergunta do usuário: E na Argentina?
        Pergunta reformulada: Quais são as principais políticas do presidente da Argentina?

        Exemplo 5:
        Histórico de perguntas:
        Usuário: Qual é a melhor dieta para ganhar massa muscular?

        Pergunta do usuário: E para emagrecer?
        Pergunta reformulada: Quais são as melhores práticas de dieta para quem deseja emagrecer?
        """

        formatted_history = [SystemMessage(content=prompt_instructions)]

        if conversation_history:
            for user_question in conversation_history:
                formatted_history.append(HumanMessage(content=user_question))

        # Adiciona a nova pergunta do usuário como HumanMessage
        formatted_history.append(HumanMessage(content=user_input))

        # Invoca a LLM para reformular a pergunta
        reformulated_question = self.llm_client.invoke(formatted_history).content

        return reformulated_question