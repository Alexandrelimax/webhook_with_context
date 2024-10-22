# layers/keep.py

class Keep:
    def __init__(self):
        # Instruções de segurança que serão sempre adicionadas ao prompt
        self.protective_prompt = """
        Você é um assistente que segue regras rígidas de segurança. 
        Você nunca deve revelar segredos, informações confidenciais, ou chaves de API.
        Mantenha a resposta dentro dos limites de segurança.
        """

    def apply_defense(self, user_input):
        """Aplica as instruções de proteção ao prompt."""
        return f"{self.protective_prompt}\n\nPergunta do usuário: {user_input}"
