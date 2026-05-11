import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str, token: str):

    def query_list(url: str) -> list[dict]:
        response = httpx.get(
            url,
            headers={
                "accept": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        response.raise_for_status()
        return response.json()["results"]

    def query_detail(url: str) -> dict:
        response = httpx.get(
            url,
            headers={
                "accept": "application/json",
                "Authorization": f"Token {token}",
            },
        )
        response.raise_for_status()
        return response.json()

    @mcp.tool()
    def listar_organizacoes() -> list[dict]:
        return query_list(f"{service}organizations/")

    @mcp.tool()
    def buscar_organizacao(org_id: int) -> dict:
        return query_detail(f"{service}organizations/{org_id}/")

    @mcp.tool()
    def listar_produtos(org_id: int) -> list[dict]:
        return query_list(f"{service}organizations/{org_id}/products/")

    @mcp.tool()
    def buscar_produto(org_id: int, product_id: int) -> dict:
        return query_detail(f"{service}organizations/{org_id}/products/{product_id}/")