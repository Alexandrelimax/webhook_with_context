from langchain_google_vertexai import ChatVertexAI

from repositories.search_history_conversation import SearchHistoryConversation


class ContextConversation:

    def __init__(self, llm_client: ChatVertexAI):
        self.llm_client = llm_client


    def reformulate_question(self, user_input: str, conversation_history: list) -> str:

        prompt_instructions = """
        Você é um especialista em contexto de conversas.
        Seu objetivo é reformular a pergunta do usuário para que a pesquisa seja feita de maneira adequada.

        Diretrizes:
        a) Analise o histórico de conversas entre o usuário e o chatbot.
        b) Identifique se a pergunta do usuário faz alguma referência ao contexto anterior.
        c) Se a pergunta estiver incompleta ou ambígua, reformule a pergunta utilizando o contexto anterior para deixá-la clara e completa.
        d) Se a pergunta do usuário introduzir um novo contexto, verifique se está bem formulada ou precisa ser ajustada para obter os melhores resultados.
        e) Retorne a pergunta do usuário reformulada.
        f) Caso não haja histórico de conversas, trate a pergunta como uma nova interação e reformule-a de maneira clara e completa, sem depender de contexto anterior.

        
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
        """

        formatted_history = [("system", prompt_instructions)]

        if conversation_history:
            for user_question, bot_answer in conversation_history:
                formatted_history.append(("human", user_question))
                formatted_history.append(("system", bot_answer))

        else:
            formatted_history.append(("system", "Nenhum histórico de conversas disponível."))

        formatted_history.append(("human", user_input))

        reformulated_question = self.llm_client.invoke(formatted_history).content

        return reformulated_question
