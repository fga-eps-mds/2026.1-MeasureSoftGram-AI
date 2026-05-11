from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def buscar_release_config_atual(organization_pk: int, product_pk: int) -> dict:
        """Retorna a configuração de release atual de um produto."""
        return client.query_detail(f"{client.service}organizations/{organization_pk}/products/{product_pk}/current/release-config/")

    @mcp.tool()
    def listar_releases(organization_pk: int, product_pk: int) -> list[dict]:
        """Lista todas as releases de um produto."""
        return client.query_list(f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/")

    @mcp.tool()
    def verificar_release_valido(organization_pk: int, product_pk: int) -> dict:
        """Verifica se a release atual é válida."""
        return client.query_detail(f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/is-valid/")

    @mcp.tool()
    def buscar_release(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna os detalhes de uma release específica."""
        return client.query_detail(f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/")

    @mcp.tool()
    def buscar_analysis_data_release(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna os dados de análise de uma release."""
        return client.query_detail(f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/analysis_data/")

    @mcp.tool()
    def buscar_planned_x_accomplished(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna o comparativo entre planejado e realizado de uma release."""
        return client.query_detail(f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/planeed-x-accomplished/")