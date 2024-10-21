from langchain_core.prompts.prompt import PromptTemplate
from typing import Any

class ContextConversationPrompt:
    "Gera uma pergunta refinada para a pesquisa de documentos usando uma LLM com exemplos de few-shot learning."

    def __init__(self, llm_client: Any):
        self.llm_client = llm_client
        self.template_str = """
        Você é um especialista em contexto de conversas.
        Seu objetivo é reformular a pergunta do usuário para que a pesquisa seja feita de maneira adequada.

        Diretrizes:
        a) Analise o histórico de conversas entre o usuário e o chatbot.
        b) Identifique se a pergunta do usuário faz alguma referência ao contexto anterior.
        c) Se a pergunta estiver incompleta ou ambígua, reformule a pergunta utilizando o contexto anterior para deixá-la clara e completa.
        d) Se a pergunta do usuário introduzir um novo contexto, verifique se está bem formulada ou precisa ser ajustada para obter os melhores resultados.
        e) Retorne a pergunta do usuário reformulada.

        Exemplos:

        Exemplo 1:
        Histórico de conversas:
        Usuário: Quem é o presidente do Brasil?
        Bot: O presidente do Brasil é o Presidente Lula.
        
        Pergunta do usuário: E da Argentina?
        Pergunta reformulada: Quem é o presidente da Argentina?

        Exemplo 2:
        Histórico de conversas:
        Usuário: Qual é o valor do dólar hoje?
        Bot: O valor do dólar hoje é R$ 5,25.
        
        Pergunta do usuário: Qual foi o valor ontem?
        Pergunta reformulada: Qual foi o valor do dólar ontem?

        Exemplo 3:
        Histórico de conversas:
        Usuário: Qual é a previsão do tempo para amanhã em São Paulo?
        Bot: A previsão do tempo para amanhã em São Paulo é de sol com algumas nuvens.
        
        Pergunta do usuário: E no Rio de Janeiro?
        Pergunta reformulada: Qual é a previsão do tempo para amanhã no Rio de Janeiro?

        Exemplo 4:
        Histórico de conversas:
        Usuário: Como funciona o sistema de pontos da empresa?
        Bot: O sistema de pontos permite que você acumule pontos em cada compra realizada.

        Pergunta do usuário: E como eu uso esses pontos?
        Pergunta reformulada: Como posso usar os pontos acumulados no sistema da empresa?

        Exemplo 5:
        Histórico de conversas:
        Usuário: Qual é a capital do Japão?
        Bot: A capital do Japão é Tóquio.
        
        Pergunta do usuário: Qual a cidade mais populosa?
        Pergunta reformulada: Qual é a cidade mais populosa do Japão?

        Histórico de conversas:
        {conversation_history}

        Pergunta do usuário:
        {user_input}

        Resposta reformulada:
        """

    def generate_answer(self, user_input: str, conversation_history: str) -> str:
        # Se não houver histórico, considera que não há contexto
        conversation_history = conversation_history if conversation_history else "Nenhum histórico de conversas disponível."
        
        # Gera o prompt a partir do template
        prompt = PromptTemplate.from_template(self.template_str)
        
        # Invoca a LLM para gerar a resposta reformulada
        return prompt.invoke({
            'user_input': user_input,
            'conversation_history': conversation_history
        }) | self.llm_client
