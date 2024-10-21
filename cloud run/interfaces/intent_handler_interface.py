from abc import ABC, abstractmethod
from typing import Dict

class IntentHandlerInterface(ABC):
    @abstractmethod
    def handle(self, fulfillment_text: str) -> Dict[str, str]:
        pass
