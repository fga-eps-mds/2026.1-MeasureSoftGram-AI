from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_organizacoes() -> list[dict]:
        """Lista todas as organizações disponíveis."""
        return client.query_list(f"{client.service}organizations/")

    @mcp.tool()
    def buscar_organizacao(org_id: int) -> dict:
        """Retorna os detalhes de uma organização pelo seu ID."""
        return client.query_detail(f"{client.service}organizations/{org_id}/")

    @mcp.tool()
    def listar_produtos(org_id: int) -> list[dict]:
        """Lista todos os produtos de uma organização."""
        return client.query_list(f"{client.service}organizations/{org_id}/products/")

    @mcp.tool()
    def buscar_produto(org_id: int, product_id: int) -> dict:
        """Retorna os detalhes de um produto pelo seu ID."""
        return client.query_detail(
            f"{client.service}organizations/{org_id}/products/{product_id}/"
        )
