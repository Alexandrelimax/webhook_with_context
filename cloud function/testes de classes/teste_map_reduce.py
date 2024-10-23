import os
import vertexai
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain_google_vertexai import VertexAI
from retrievers.unstructured_retriever import UnstructuredRetriever
from retrievers.map_reduce_retriever import MapReduceRetrieverWithReferences


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

# project_id = ""
# region = "us-central1"
# datastore_id = "ascensao_"
# location = 'global'

# vertexai.init(project=project_id, location=region)
# llm_client = VertexAI(model_name="gemini-1.5-flash-001", temperature=1, top_p=0.95, max_output_token=2000
#     ) # Ou outro LLM como Vertex AI
# retriever = UnstructuredRetriever()  # Substitua por uma instância do seu retriever implementado
# document_prompt_template = PromptTemplate(input_variables=["context"], template="Resumo do documento: {context}")
# map_prompt_template = PromptTemplate(input_variables=["context"], template="Resuma o seguinte conteúdo: {context}")
# reduce_prompt_template = PromptTemplate(input_variables=["context"], template="Combine os seguintes resumos: {context}")

# # Inicializa o MapReduceRetrieverWithReferences
# map_reduce_retriever = MapReduceRetrieverWithReferences(
#     llm=llm_client,
#     retriever=retriever,
#     document_prompt_template=document_prompt_template,
#     map_prompt_template=map_prompt_template,
#     reduce_prompt_template=reduce_prompt_template
# )

# # Pergunta do usuário
# user_input = "Quais são os impactos da mudança climática na economia?"

# # Chama o método retrieve_and_combine para obter o resultado
# result = map_reduce_retriever.retrieve_and_combine(user_input)

# # Exibe o resultado final e as referências
# print("Resposta:", result["answer"])
# print("Referências:")
# for ref in result["references"]:
#     print(f"- ID: {ref['doc_id']}, Título: {ref['title']}, URL: {ref['url']}")




from typing import Any, Dict, List, Tuple
from langchain.schema import BaseRetriever, Document

class MapReduceRetrieverWithReferences:
    def __init__(self, llm: Any, retriever: BaseRetriever, document_prompt_template: Any, map_prompt_template: Any, reduce_prompt_template: Any):
        self.retriever = retriever
        self.chain_builder = MapReduceChainBuilder(
            llm=llm,
            document_prompt_template=document_prompt_template,
            map_prompt_template=map_prompt_template,
            reduce_prompt_template=reduce_prompt_template
        )
        self.map_reduce_chain = self.chain_builder.create_map_reduce_chain()

    def retrieve_and_combine(self, user_input: str) -> Dict[str, Any]:
        docs = self.retriever.get_relevant_documents(user_input)
        result = self.map_reduce_chain.invoke({"context": docs})
        references = ReferenceFormatter.format_references(docs)

        return {
            "answer": result,
            "references": references
        }
