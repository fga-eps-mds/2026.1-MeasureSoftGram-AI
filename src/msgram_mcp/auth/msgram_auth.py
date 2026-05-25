import httpx


def msgram_auth(service: str, user: str, password: str) -> str:
    response = httpx.post(
        f"{service}accounts/login/",
        json={"username": user, "password": password},
        headers={"accept": "application/json"},
    )
    response.raise_for_status()
    return response.json()["key"]
