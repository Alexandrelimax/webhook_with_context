# layers/wall.py
import re

class Wall:
    def __init__(self, blocked_keywords=None):
        if blocked_keywords is None:
            self.blocked_keywords = ["ignore", "bypass", "reveal", "secret", "password"]
        else:
            self.blocked_keywords = blocked_keywords

    def sanitize_input(self, user_input):
        """Remove ou alerta sobre padrões maliciosos no input."""
        # Verifica palavras-chave bloqueadas
        for keyword in self.blocked_keywords:
            if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
                raise ValueError(f"Prompt contém palavra-chave bloqueada: '{keyword}'")

        # Verifica por PII como emails
        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", user_input):
            raise ValueError("Prompt contém informação sensível (e-mail).")

        return user_input
