# layers/drawbridge.py

class Drawbridge:
    def __init__(self, allow_unsafe_scripts=False):
        self.allow_unsafe_scripts = allow_unsafe_scripts

    def validate_response(self, response):
        """Verifica a resposta por padrões perigosos ou não seguros."""
        if not self.allow_unsafe_scripts and ("<script>" in response or "</script>" in response):
            raise ValueError("Resposta contém script perigoso.")
        
        # Verifica a presença de chaves secretas (exemplo: 'API_KEY')
        if "API_KEY" in response:
            raise ValueError("Resposta contém informações sensíveis.")
        
        return response
