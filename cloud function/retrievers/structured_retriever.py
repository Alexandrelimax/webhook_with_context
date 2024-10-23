from langchain_google_community import VertexAISearchRetriever
# from retrievers.base_retriever import BaseRetriever

class StructuredRetriever(VertexAISearchRetriever):
    def __init__(self, project_id: str, location_id: str, data_store_id: str, max_documents: int = 3):
        super().__init__(
            project_id=project_id,
            location_id=location_id,
            data_store_id=data_store_id,
            max_documents=max_documents,
            engine_data_type=1  # Definido para dados estruturados
        )
