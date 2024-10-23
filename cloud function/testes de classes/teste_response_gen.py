import os
import vertexai

from retrievers.unstructured_retriever import UnstructuredRetriever
from langchain_google_vertexai import ChatVertexAI
from core.response_generator import ResponseGenerator
from langchain_core.documents import Document
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

project_id = ""
region = "us-central1"
datastore_id = "ascensao_"
location = 'global'


#Configurações de teste
llm_client = ChatVertexAI(model="gemini-1.5-flash-001", temperature=0.7, max_tokens=2000)
response_generator = ResponseGenerator(llm_client)

# Dados de teste
user_input = "Quais são as práticas recomendadas para empresas em relação à sustentabilidade?"
conversation_history = [
    ("Quais são os impactos das mudanças climáticas?", "Os impactos incluem aumento do nível do mar, eventos climáticos extremos e perda de biodiversidade.")
]

# Documento de teste
relevant_documents = [
    Document(page_content="As empresas devem adotar práticas sustentáveis, como o uso de energias renováveis e a promoção de uma economia circular.", 
             metadata={"title": "Práticas Sustentáveis para Empresas"})
]

# Gerar a resposta
response = response_generator.generate_response(user_input, conversation_history, relevant_documents)
print("Resposta gerada:", response)