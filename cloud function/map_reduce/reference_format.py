from langchain.schema import Document
from typing import List, Dict

class ReferenceFormatter:
    @staticmethod
    def format_references(docs: List[Document]) -> List[Dict[str, str]]:
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
        return doc_references
