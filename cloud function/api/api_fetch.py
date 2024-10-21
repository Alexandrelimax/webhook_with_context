import requests

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str, params: dict = None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

# Exemplo de uso:
# client = APIClient("https://api.exemplo.com")
# response = client.get("dados", params={"id": "12345"})
# print(response)
