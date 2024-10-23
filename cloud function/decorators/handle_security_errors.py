from functools import wraps

def handle_security_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            # Lida com erros de segurança
            print(f"Erro de segurança: {e}")
            error_message = "Desculpe, não posso fornecer essas informações. Posso ajudar com outra coisa?"
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