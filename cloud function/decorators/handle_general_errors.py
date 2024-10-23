from functools import wraps

def handle_general_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Lida com erros gerais
            print(f"Erro ao processar a requisição: {e}")
            error_message = "Houve um problema ao processar sua solicitação. Tente novamente mais tarde."
            response = {
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": [
                                    error_message
                                ]
                            }
                        }
                    ]
                }
            }
            return (response, 200, {'Content-Type': 'application/json'})
    return wrapper
