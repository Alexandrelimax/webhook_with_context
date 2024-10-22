from langchain_google_community import VertexAISearchRetriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_vertexai import VertexAI
import vertexai
from prompts.retrieval_qa_prompt import retrieval_qa_chat_prompt



def format_answer(qa_retriever):
    return qa_retriever.get('answer', 'Não foi possivel processar sua resposta')


def retriever_qa_with_sources(user_input, datastore_id):
    vertexai.init(project_id=project_id, location=location)
    llm = VertexAI(model_name=model, temperature=temperature, top_p=top_p, max_output_token=max_output_token)

    retriever = VertexAISearchRetriever(project_id=project_id, location=location, datastore_id=datastore_id)

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt, )

    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return retrieval_chain.invoke({'input': user_input})
