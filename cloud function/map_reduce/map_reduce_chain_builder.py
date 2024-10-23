from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.map_reduce import ReduceDocumentsChain, MapReduceDocumentsChain
from typing import Any

class MapReduceChainBuilder:
    def __init__(self, llm: Any, document_prompt_template: Any, map_prompt_template: Any, reduce_prompt_template: Any):
        self.llm = llm
        self.document_prompt_template = document_prompt_template
        self.map_prompt_template = map_prompt_template
        self.reduce_prompt_template = reduce_prompt_template

    def create_map_reduce_chain(self) -> MapReduceDocumentsChain:
        llm_chain_map = self._create_llm_chain(self.map_prompt_template)
        llm_chain_reduce = self._create_llm_chain(self.reduce_prompt_template)
        combine_documents_chain = self._create_combine_documents_chain(llm_chain_map)
        reduce_documents_chain = self._create_reduce_documents_chain(combine_documents_chain, llm_chain_reduce)

        return MapReduceDocumentsChain(
            llm_chain=llm_chain_map,
            reduce_documents_chain=reduce_documents_chain
        )

    def _create_llm_chain(self, prompt_template: Any) -> LLMChain:
        return LLMChain(llm=self.llm, prompt=prompt_template)

    def _create_combine_documents_chain(self, llm_chain: LLMChain) -> StuffDocumentsChain:
        return StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=self.document_prompt_template,
            document_variable_name="context"
        )

    def _create_reduce_documents_chain(self, combine_documents_chain: StuffDocumentsChain, llm_chain_reduce: LLMChain) -> ReduceDocumentsChain:
        return ReduceDocumentsChain(
            combine_documents_chain=combine_documents_chain,
            llm_chain=llm_chain_reduce
        )
