from langchain_google_vertexai import ChatVertexAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage  # Importação necessária para mensagens estruturadas

class ContextConversation:
    def __init__(self, llm_client: ChatVertexAI):
        self.llm_client = llm_client

    def reformulate_question(self, user_input: str, conversation_history: list) -> str:

        prompt_instructions = """
        Você é um especialista em reformular perguntas de conversas.

        Seu único objetivo é reformular a pergunta do usuário de forma clara e direta, sem fornecer respostas ou informações adicionais. Apenas transforme a pergunta para torná-la mais completa, sem introduzir novos dados, recomendações ou respostas.

        Diretrizes:
        a) Reformule a pergunta do usuário sem fornecer respostas diretas ou conteúdo adicional. Sua tarefa é apenas tornar a pergunta clara e objetiva.
        b) Use o contexto anterior apenas para melhorar a clareza e a completude da pergunta, sem criar novas informações, suposições ou recomendações.
        c) Certifique-se de que a pergunta reformulada seja sobre o que o usuário deseja saber, sem adicionar detalhes novos ou suposições.
        d) Não forneça conselhos, recomendações ou respostas como parte da reformulação.
        e) Caso não haja histórico de conversas, trate a pergunta como uma nova interação.

        Exemplos de perguntas reformuladas:
        Exemplo 1:
        Histórico de conversas:
        Usuário: Quem é o presidente do Brasil?
        Bot: O presidente do Brasil é o Presidente Lula.

        Pergunta do usuário: E da Argentina?
        Pergunta reformulada: Quem é o presidente da Argentina?

        Exemplo 2:
        Histórico de conversas:
        Usuário: Qual é a capital do Japão?
        Bot: A capital do Japão é Tóquio.

        Pergunta do usuário: Qual a cidade mais populosa?
        Pergunta reformulada: Qual é a cidade mais populosa do Japão?

        Exemplo 3:
        Histórico de conversas:
        Usuário: Como funciona o sistema de pontos da empresa?
        Bot: O sistema de pontos permite que você acumule pontos em cada compra realizada.

        Pergunta do usuário: E como eu uso esses pontos?
        Pergunta reformulada: Como posso usar os pontos acumulados no sistema da empresa?

        Exemplo 4:
        Histórico de conversas:
        Usuário: Quais são as principais políticas do Presidente Lula?
        Bot: As principais políticas do Presidente Lula são focadas em áreas sociais, econômicas e ambientais.

        Pergunta do usuário: E na Argentina?
        Pergunta reformulada: Quais são as principais políticas do presidente da Argentina?
        """

        # Substituir as tuplas por instâncias das classes de mensagem
        formatted_history = [SystemMessage(content=prompt_instructions)]

        if conversation_history:
            for user_question, bot_answer in conversation_history:
                formatted_history.append(HumanMessage(content=user_question))
                formatted_history.append(AIMessage(content=bot_answer))


        formatted_history.append(HumanMessage(content=user_input))

        # Invoca a LLM para reformular a pergunta
        reformulated_question = self.llm_client.invoke(formatted_history).content

        return reformulated_question
