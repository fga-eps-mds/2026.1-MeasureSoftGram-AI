import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str, token: str):

    def query_list(url: str) -> list[dict]:
        response = httpx.get(
            url,
            headers={"accept": "application/json", "Authorization": f"Token {token}"},
        )
        response.raise_for_status()
        data = response.json()
        return data["results"] if "results" in data else data

    def query_detail(url: str) -> dict:
        response = httpx.get(
            url,
            headers={"accept": "application/json", "Authorization": f"Token {token}"},
        )
        response.raise_for_status()
        return response.json()

    @mcp.tool()
    def buscar_release_config_atual(organization_pk: int, product_pk: int) -> dict:
        """Retorna a configuração de release atual de um produto."""
        return query_detail(f"{service}organizations/{organization_pk}/products/{product_pk}/current/release-config/")

    @mcp.tool()
    def listar_releases(organization_pk: int, product_pk: int) -> list[dict]:
        """Lista todas as releases de um produto."""
        return query_list(f"{service}organizations/{organization_pk}/products/{product_pk}/release/")

    @mcp.tool()
    def verificar_release_valido(organization_pk: int, product_pk: int) -> dict:
        """Verifica se a release atual é válida."""
        return query_detail(f"{service}organizations/{organization_pk}/products/{product_pk}/release/is-valid/")

    @mcp.tool()
    def buscar_release(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna os detalhes de uma release específica."""
        return query_detail(f"{service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/")

    @mcp.tool()
    def buscar_analysis_data_release(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna os dados de análise de uma release."""
        return query_detail(
            f"{service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/analysis_data/")

    @mcp.tool()
    def buscar_planned_x_accomplished(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna o comparativo entre planejado e realizado de uma release."""
        return query_detail(
            f"{service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/planeed-x-accomplished/")
