import os
import vertexai
from langchain_google_vertexai import VertexAI
from langchain.prompts.prompt import PromptTemplate
from langchain_google_community import VertexAISearchRetriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_account.json'

project_id = ""
region = "us-central1"
datastore_id = "ascensao_"
location = 'global'
model = 'gemini-1.5-flash'
temperature = 1
top_p = 0.9
max_output_token = 2000

retrieval_qa_chat_prompt = PromptTemplate.from_template("""
    Crie um prompt aqui!

    <context>
    {context}
    </context>

    <question>
    {input}
    </question>
""")


def format_answer(qa_retriever):
    return qa_retriever.get('answer', 'Não foi possivel processar sua resposta')


def retriever_qa_with_sources(user_input, datastore_id):
    vertexai.init(project_id=project_id, location=location)
    llm = VertexAI(model_name=model, temperature=temperature, top_p=top_p, max_output_token=max_output_token)

    retriever = VertexAISearchRetriever(project_id=project_id, location=location, datastore_id=datastore_id)

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt, )

    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return retrieval_chain.invoke({'input': user_input})
