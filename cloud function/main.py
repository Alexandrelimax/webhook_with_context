import uvicorn
from fastapi import FastAPI

from langchain_google_vertexai import ChatVertexAI
from controllers.webhook_controller import WebhookController
from retrievers.structured_retriever import StructuredRetriever


app = FastAPI()

project_id = ""
region = "us-central1"
datastore_id = "3541312121684351asd"


llm_client = ChatVertexAI(model="gemini-1.5-flash-001", temperature=0)

structured_retriever = StructuredRetriever(project_id=project_id, location_id=region, data_store_id=datastore_id)

webhook_controller = WebhookController(project_id=project_id, llm_client=llm_client, retriever=structured_retriever)


app.include_router(webhook_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
