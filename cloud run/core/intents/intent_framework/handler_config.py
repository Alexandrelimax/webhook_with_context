from core.intents.intent_framework import HandlerFactory
from core.intents.intent_implementations.order_status import OrderStatusHandler
from core.intents.intent_implementations.list_products import ProductsHandler


"""Configura os handlers disponíveis e os registra na fábrica."""
def configure_handlers() -> HandlerFactory:
    factory = HandlerFactory()
    factory.register_handler('list_products', ProductsHandler)
    factory.register_handler('order_status', OrderStatusHandler)
    return factory
