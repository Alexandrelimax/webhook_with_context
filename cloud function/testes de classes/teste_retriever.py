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


vertexai.init(project=project_id, location=region)


llm_client= ChatVertexAI(
    model="gemini-1.5-flash-001",
    temperature=1,
    max_tokens=2000,
    max_retries=3,
    stop=None,
    )
query = 'As empresas, em particular, estão sob crescente pressão'

unstructured_retriever = UnstructuredRetriever(project_id=project_id, location_id=location, data_store_id=datastore_id)

result = unstructured_retriever.invoke(query)

for doc in result:
    print(doc)