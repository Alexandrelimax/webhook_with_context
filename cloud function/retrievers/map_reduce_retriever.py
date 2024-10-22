from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.chains.llm import LLMChain


class MapReduceRetrieverWithReferences:
    def __init__(self, llm, retriever, document_prompt_template, map_prompt_template, reduce_prompt_template):
        self.llm = llm
        self.retriever = retriever
        self.document_prompt_template = document_prompt_template
        self.map_prompt_template = map_prompt_template
        self.reduce_prompt_template = reduce_prompt_template
        self.map_reduce_chain = self._initialize_map_reduce_chain()


    def _initialize_map_reduce_chain(self):    
        # Cadeia LLM para processar cada documento individualmente (Map Step)
        llm_chain_map = LLMChain(llm=self.llm, prompt=self.map_prompt_template)

        # Cadeia LLM para combinar os resumos gerados (Reduce Step)
        llm_chain_reduce = LLMChain(llm=self.llm, prompt=self.reduce_prompt_template)

        # Cadeia para formatar e combinar documentos no Map Step
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=llm_chain_map,
            document_prompt=self.document_prompt_template,
            document_variable_name="context"
        )

        # Cadeia de redução para combinar os documentos após o map step
        reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            llm_chain=llm_chain_reduce  # Usando o reduce_prompt_template aqui
        )

        # Cadeia Map-Reduce para processar os documentos e gerar as respostas
        map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=llm_chain_map,  # Cadeia Map
            reduce_documents_chain=reduce_documents_chain  # Cadeia Reduce
        )
        
        return map_reduce_chain

    def retrieve_and_combine(self, user_input: str):
        # Recupera os documentos relevantes
        docs = self.retriever.get_relevant_documents(user_input)

        # Chama a cadeia Map-Reduce com os documentos
        result, doc_references = self.map_reduce_chain.invoke({"context": docs})

        # Retorna o resultado final e as referências dos documentos
        return result, doc_references

    def format_response_with_references(self, result, docs):
        # Formatar a resposta com as referências
        doc_references = []
        for doc in docs:
            doc_id = doc.metadata.get('doc_id', 'Unknown')
            title = doc.metadata.get('title', 'Sem título')
            url = doc.metadata.get('url', 'Unknown')
            doc_references.append({
                "doc_id": doc_id,
                "title": title,
                "url": url
            })
        
        response_dict = {
            "answer": result,
            "references": doc_references
        }

        return response_dict
