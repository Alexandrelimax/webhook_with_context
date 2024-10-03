from typing import Dict

class PromptManager:
    def __init__(self):
        self.prompts: Dict[str, str] = {}

    def add_prompt(self, key: str, prompt: str):
        self.prompts[key] = prompt

    def get_prompt(self, key: str) -> str:
        return self.prompts.get(key, "Prompt não encontrado.")
