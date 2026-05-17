from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_todos_objetivos(organization_pk: int, product_pk: int) -> list[dict]:
        """Lista todos os objetivos cadastrados de um produto."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/all/goal/"
        )

    @mcp.tool()
    def buscar_objetivo_atual(organization_pk: int, product_pk: int) -> dict:
        """Retorna o objetivo atual de um produto."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/current/goal/"
        )

    @mcp.tool()
    def buscar_pre_config_padrao(organization_pk: int, product_pk: int) -> dict:
        """Retorna a pré-configuração padrão de um produto."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/default/pre-config/"
        )
