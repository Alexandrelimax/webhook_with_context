import redis
from typing import Dict, Any

class RedisRepository:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        # Inicializa a conexão com o Redis diretamente na classe
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.max_interactions = 15  # Define o número máximo de interações

    def add_interaction(self, user_id: str, user_message: str, bot_response: str):
        key = f"chat_history:{user_id}"
        new_interaction = {"role": "user", "message": user_message}
        bot_interaction = {"role": "bot", "message": bot_response}

        # Adiciona as interações ao Redis
        self.redis.lpush(key, new_interaction)
        self.redis.lpush(key, bot_interaction)

        # Limita o tamanho da lista
        self.redis.ltrim(key, 0, self.max_interactions * 2 - 1)

    def get_history(self, user_id: str) -> Dict[str, Any]:
        key = f"chat_history:{user_id}"
        return self.redis.lrange(key, 0, -1)  # Retorna todas as interações
