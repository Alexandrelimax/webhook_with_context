from langchain.prompts.prompt import PromptTemplate

retrieval_qa_chat_prompt = PromptTemplate.from_template("""
    Crie um prompt aqui!

    <context>
    {context}
    </context>

    <question>
    {input}
    </question>
""")