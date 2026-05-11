import httpx

class MsgramClient:
    def __init__(self, service: str, token: str):
        self.service = service
        self._auth_headers = {
            "accept": "application/json",
            "Authorization": f"Token {token}",
        }
        self._public_headers = {
            "accept": "application/json",
        }

    def _get(self, url: str, public: bool = False) -> httpx.Response:
        headers = self._public_headers if public else self._auth_headers
        response = httpx.get(url, headers=headers)
        if response.status_code == 500:
            raise RuntimeError("Erro interno no servidor.")
        response.raise_for_status()
        return response

    def query_list(self, url: str, public: bool = False) -> list[dict]:
        data = self._get(url, public=public).json()
        return data["results"] if "results" in data else data

    def query_detail(self, url: str, public: bool = False) -> dict:
        return self._get(url, public=public).json()