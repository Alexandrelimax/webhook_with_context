import re
import logging

class WallDefender:
    def __init__(self, blocked_keywords=None):
        if blocked_keywords is None:
            self.blocked_keywords = [
                "ignore", "bypass", "reveal", "secret", "password",
                "API_KEY", "token", "credentials", "admin", "confidential"
            ]
        else:
            self.blocked_keywords = blocked_keywords

        # Configura logging
        logging.basicConfig(filename='security_logs.log', level=logging.INFO)

    def sanitize_input(self, user_input):
        """Remove ou alerta sobre padrões maliciosos no input."""
        # Verifica palavras-chave bloqueadas
        for keyword in self.blocked_keywords:
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                logging.warning(f"Attempted use of blocked keyword: '{keyword}'")
                raise ValueError(f"Prompt contém palavra-chave bloqueada: '{keyword}'")

        # Verifica por PII como emails e números de telefone
        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", user_input):
            logging.warning("Prompt contém informação sensível (e-mail).")
            raise ValueError("Prompt contém informação sensível (e-mail).")
        if re.search(r"\b\d{10,11}\b", user_input):
            logging.warning("Prompt contém possível número de telefone.")
            raise ValueError("Prompt contém possível número de telefone.")

        # Verifica por padrões de CPF (BR)
        if re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", user_input):
            logging.warning("Prompt contém possível CPF.")
            raise ValueError("Prompt contém informação sensível (CPF).")

        return user_input
