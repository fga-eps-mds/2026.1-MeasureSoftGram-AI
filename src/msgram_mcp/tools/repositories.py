from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_repositorios(organization_pk: int, product_pk: int) -> list[dict]:
        """Lista todos os repositórios de um produto."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/"
        )

    @mcp.tool()
    def buscar_repositorio(
        organization_pk: int, product_pk: int, repository_id: int
    ) -> dict:
        """Retorna os detalhes de um repositório pelo seu ID."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_id}/"
        )

    @mcp.tool()
    def buscar_arvore_relacionamentos_produto(
        organization_pk: int, product_pk: int
    ) -> list[dict]:
        """Retorna as entidades de uma pré-configuração e suas relações no formato de árvore."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/entity-relationship-tree/"
        )

    @mcp.tool()
    def listar_tsqmi_historico_repositorios(
        organization_pk: int, product_pk: int
    ) -> list[dict]:
        """Lista o histórico de TSQMI de todos os repositórios de um produto."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories-tsqmi-historical-values/"
        )

    @mcp.tool()
    def listar_tsqmi_recente_repositorios(
        organization_pk: int, product_pk: int
    ) -> list[dict]:
        """Lista o TSQMI mais recente de todos os repositórios de um produto."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories-tsqmi-latest-values/"
        )
