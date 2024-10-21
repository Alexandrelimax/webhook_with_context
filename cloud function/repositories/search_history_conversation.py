from google.cloud import bigquery


class SearchHistoryConversation:
    def __init__(self, project_id: str, session_id: str):
        self.bigquery_client = bigquery.Client(project=project_id)
        self.session_id = session_id


    def get_last_turns(self, limit: int = 5):
        query = """
        SELECT 
            JSON_EXTRACT_SCALAR(request, '$.queryInput.text.text') AS user_question,
            JSON_EXTRACT_SCALAR(response, '$.queryResult.responseMessages[0].text.text[0]') AS chatbot_answer,
            turn_position
        FROM `dialogflow_history.dialogflow_bigquery_export_data`
        WHERE conversation_name = @session_id
        ORDER BY turn_position DESC
        LIMIT @limit
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("session_id", "STRING", self.session_id),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
        )

        query_job = self.bigquery_client.query(query, job_config=job_config)
        results = query_job.result()

        history = [(row["user_question"], row["chatbot_answer"]) for row in results]
        
        return history if history else []
