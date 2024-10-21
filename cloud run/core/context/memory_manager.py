class MemoryManager:
    def __init__(self, redis_repository: RedisRepository):
        self.redis_repository = redis_repository

    def add_memory(self, user_id: str, user_message: str, bot_response: str):
        self.redis_repository.add_interaction(user_id, user_message, bot_response)

    def get_memory(self, user_id: str):
        return self.redis_repository.get_history(user_id)

# Exemplo de uso
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
# memory_manager = MemoryManager(redis_client)

# Adicionando interações
# memory_manager.add_interaction(user_id="123", user_message="Olá!", bot_response="Olá! Como posso ajudar?")
# memory_manager.add_interaction(user_id="123", user_message="Qual é o tempo hoje?", bot_response="Hoje está ensolarado.")
