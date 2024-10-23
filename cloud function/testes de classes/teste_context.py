import os
from langchain_google_vertexai import ChatVertexAI

from core.context_conversation import ContextConversation

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

project_id = ""
region = "us-central1"
datastore_id = "ascensao_"
location = 'global'



# llm_client = ChatVertexAI(model="gemini-1.5-flash-001", temperature=0.7, max_tokens=150)
llm_client = ChatVertexAI(model="gemini-1.0-pro", temperature=0.8, max_tokens=150, top_p = 0.9)

context_conversation = ContextConversation(llm_client=llm_client)


# user_input = "E como são na Argentina?"
# conversation_history = [
#     ("Quem é o presidente do Brasil?", "O presidente do Brasil é o Presidente Lula."),
#     ("Quais são as principais políticas dele?", "O Presidente Lula foca em políticas sociais, econômicas e ambientais.")
# ]
user_input = "E quais estratégias devo usar?"
conversation_history = [
    ("Como faço para criar uma campanha de marketing digital?", 
     "Você pode criar uma campanha de marketing digital definindo seu público-alvo, estabelecendo objetivos claros, criando conteúdo relevante e escolhendo as plataformas certas para distribuição."),
    ("Quais são as melhores plataformas?", 
     "As melhores plataformas dependem do seu público, mas geralmente incluem Facebook, Instagram, Google Ads e LinkedIn."),
    ("E para o setor de tecnologia?", 
     "No setor de tecnologia, LinkedIn e Google Ads são altamente recomendados por serem mais focados em um público profissional.")
]

# user_input_1 = "E para investimentos?"
# conversation_history_1 = [
#     ("Como posso melhorar meu planejamento financeiro?", 
#      "Você pode começar acompanhando suas receitas e despesas, definindo um orçamento e estabelecendo metas de economia."),
#     ("Qual é o melhor método para isso?", 
#      "Métodos como planilhas financeiras, aplicativos de controle de despesas e a regra 50-30-20 são opções populares.")
# ]

user_input_4 = "E após o treino?"
conversation_history_4 = [
    "Quais são os melhores exercícios para fortalecer as pernas?",
    "E para ganhar massa muscular nas pernas?",
    "Qual a importância do aquecimento antes dos exercícios?",
    "E como devo fazer o aquecimento?",
    "Como posso evitar lesões durante o treino?"
]

# Chamada do método para reformular a pergunta com apenas as perguntas anteriores
reformulated_question_4 = context_conversation.reformulate_question(user_input_4, conversation_history_4)
print("Novo Caso de Teste - Pergunta reformulada:", reformulated_question_4)