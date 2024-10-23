import re
import logging

class DrawbridgeDefender:
    def __init__(self, allow_unsafe_scripts=False):
        self.allow_unsafe_scripts = allow_unsafe_scripts
        logging.basicConfig(filename='security_logs.log', level=logging.INFO)

    def validate_response(self, response):
        """Verifica a resposta por padrões perigosos ou não seguros."""
        if not self.allow_unsafe_scripts and ("<script>" in response or "</script>" in response):
            logging.warning("Resposta contém script perigoso.")
            raise ValueError("Resposta contém script perigoso.")
        
        # Verifica a presença de chaves secretas (exemplo: 'API_KEY')
        if "API_KEY" in response or re.search(r"\b[A-Za-z0-9]{40}\b", response):
            logging.warning("Resposta contém informações sensíveis.")
            raise ValueError("Resposta contém informações sensíveis.")
        
        # Verifica por números de cartão de crédito (detecção básica de 16 dígitos)
        if re.search(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", response):
            logging.warning("Resposta contém possível número de cartão de crédito.")
            raise ValueError("Resposta contém possível número de cartão de crédito.")

        return response
