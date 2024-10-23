import logging
import re

class KeepDefender:
    def __init__(self):
        # Prompt base de segurança, usado para qualquer situação
        self.base_protective_prompt = """
        Você é um assistente que segue regras rígidas de segurança. 
        Você nunca deve revelar segredos, informações confidenciais, ou chaves de API.
        Mantenha a resposta dentro dos limites de segurança.
        """

        # Instruções específicas para diferentes tipos de contextos
        self.context_specific_prompts = {
            "financeiro": """
            Nunca forneça informações financeiras sensíveis, como detalhes de transações bancárias, números de conta, ou credenciais financeiras.
            Mantenha suas respostas estritamente relacionadas ao tópico sem revelar qualquer dado financeiro.
            """,
            "médico": """
            Nunca forneça diagnósticos médicos ou detalhes de condições de saúde sensíveis.
            Não faça recomendações médicas, diagnósticos ou ofereça conselhos relacionados a tratamentos.
            """,
            "legal": """
            Não forneça conselhos legais, não faça suposições ou afirme leis como corretas sem uma referência precisa.
            Mantenha suas respostas neutras e informativas, sem fornecer pareceres legais.
            """
        }

        # Palavras-chave para detectar contextos sensíveis
        self.context_keywords = {
            "financeiro": ["transação", "número da conta", "saldo", "fatura", "cartão", "pagamento"],
            "médico": ["diagnóstico", "saúde", "tratamento", "doença", "medicação", "sintomas"],
            "legal": ["lei", "jurídico", "processo", "advogado", "contrato", "regulamento"]
        }

        # Configura logging
        logging.basicConfig(filename='security_logs.log', level=logging.INFO)

    def detect_context(self, user_input):
        """Detecta o contexto da conversa com base nas palavras-chave."""
        for context, keywords in self.context_keywords.items():
            if any(re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE) for keyword in keywords):
                return context
        return "geral"

    def apply_defense(self, user_input):
        """Aplica instruções de proteção ao prompt com base no contexto detectado."""
        context = self.detect_context(user_input)
        specific_instruction = self.context_specific_prompts.get(context, "")

        logging.info(f"Applying defense with detected context: {context}")

        # Combina as instruções base e específicas do contexto detectado
        return f"{self.base_protective_prompt}\n{specific_instruction}\n\nPergunta do usuário: {user_input}"
