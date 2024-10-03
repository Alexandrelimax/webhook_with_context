import os
import importlib
from core.intents.intent_framework.handler_factory import HandlerFactory
from interfaces.intent_handler_interface import IntentHandlerInterface

def configure_handlers_automatic() -> HandlerFactory:
    factory = HandlerFactory()
    
    # Diretório das implementações de intents
    intent_dir = os.path.join(os.path.dirname(__file__), "intent_implementations")

    # Caminho de import das implementações
    intent_module_path = "core.intents.intent_implementations"

    # Percorre os arquivos de implementação de intents
    for file in os.listdir(intent_dir):
        if file.endswith(".py") and file != "__init__.py":
            # Importa o módulo correspondente ao arquivo
            module_name = f"{intent_module_path}.{file[:-3]}"
            module = importlib.import_module(module_name)
            
            # Itera sobre os atributos do módulo
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Verifica se o atributo é uma classe e se implementa a interface
                if isinstance(attr, type) and issubclass(attr, IntentHandlerInterface) and attr is not IntentHandlerInterface:
                    # Registra a classe no factory usando o nome da classe como chave
                    factory.register_handler(attr_name.lower(), attr)

    return factory
