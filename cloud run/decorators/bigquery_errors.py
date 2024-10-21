from google.api_core.exceptions import GoogleAPIError

def handle_bigquery_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GoogleAPIError as e:
            print(f"Ocorreu um erro ao executar a consulta no BigQuery: {e}")
            return []
    return wrapper
