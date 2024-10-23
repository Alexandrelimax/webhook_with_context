from selectors.relevant_turn_selector import RelevantTurnSelector
from refiners.question_refiner import QuestionRefiner
from langchain_google_vertexai import ChatVertexAI

llm_client

examples = [
    {"input": "Qual é a capital da França?", "output": "A capital da França é Paris."},
    {"input": "Quem é o presidente dos EUA?", "output": "O presidente dos EUA é Joe Biden."},
    {"input": "Quais são as principais políticas dele?", "output": "As principais políticas envolvimento economia e saúde."},
    {"input": "O que é a ONU?", "output": "A ONU é a Organização das Nações Unidas."}
]
user_input = "Quais são as principais políticas do presidente dos EUA?"

turn_selector = RelevantTurnSelector(examples, k=5)
relevant_turns = turn_selector.select_relevant_turns(user_input)

llm_client = ChatVertexAI(model="gemini-1.5-flash-001", temperatura=0.7, max_tokens=100)
question_refiner = QuestionRefiner(llm_client)

reformulated_question = question_refiner.refine_question(user_input, relevant_turns)
print("Pergunta Reformulada:", reformulated_question)