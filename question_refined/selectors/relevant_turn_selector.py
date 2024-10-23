from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores.faiss import FAISS

class RelevantTurnSelector:
    def __init__(self, examples, top_k=5):
        self.top_k = top_k
        self.embeddings_model = OpenAIEmbeddings()
        self.example_selector = SemanticSimilarityExampleSelector.from_examples(examples=examples, embeddings=self.embeddings_model, vectorstore_cls=FAISS, k=self.top_k)
        

    def select_relevant_turns(self, user_input):
        relevant_examples = self.example_selector.select_examples({'input': user_input})

        relevant_turns = [(ex['input'], ex['output']) for ex in relevant_examples]

        return relevant_turns
    

    
