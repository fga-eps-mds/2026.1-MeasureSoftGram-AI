import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str, token: str):

    def query(url: str) -> list[dict]:
        response = httpx.get(
            f"{url}",
            headers={
                "accept": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        response.raise_for_status()
        return response.json()["results"]


    @mcp.tool()
    def listar_organizacoes() -> list[dict]:
        return query(f"{service}organizations/")
