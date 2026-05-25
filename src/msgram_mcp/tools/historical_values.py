from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_historico_caracteristicas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o histórico de características calculadas de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/characteristics/"
        )

    @mcp.tool()
    def buscar_historico_caracteristica(
        organization_pk: int, product_pk: int, repository_pk: int, characteristic_id: int
    ) -> dict:
        """Retorna o histórico de uma característica específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/characteristics/{characteristic_id}/"
        )

    @mcp.tool()
    def listar_historico_subcaracteristicas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o histórico de subcaracterísticas calculadas de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/subcharacteristics/"
        )

    @mcp.tool()
    def buscar_historico_subcaracteristica(
        organization_pk: int, product_pk: int, repository_pk: int, subcharacteristic_id: int
    ) -> dict:
        """Retorna o histórico de uma subcaracterística específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/subcharacteristics/{subcharacteristic_id}/"
        )

    @mcp.tool()
    def listar_historico_medidas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o histórico de medidas coletadas de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/measures/"
        )

    @mcp.tool()
    def buscar_historico_medida(
        organization_pk: int, product_pk: int, repository_pk: int, measure_id: int
    ) -> dict:
        """Retorna o histórico de uma medida específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/measures/{measure_id}/"
        )

    @mcp.tool()
    def listar_historico_metricas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o histórico de métricas coletadas de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/metrics/"
        )

    @mcp.tool()
    def buscar_historico_metrica(
        organization_pk: int, product_pk: int, repository_pk: int, metric_id: int
    ) -> dict:
        """Retorna o histórico de uma métrica específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/metrics/{metric_id}/"
        )

    @mcp.tool()
    def listar_historico_tsqmi(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o histórico de TSQMI de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/tsqmi/"
        )

    @mcp.tool()
    def buscar_historico_tsqmi(
        organization_pk: int, product_pk: int, repository_pk: int, tsqmi_id: int
    ) -> dict:
        """Retorna um registro específico do histórico de TSQMI de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/historical-values/tsqmi/{tsqmi_id}/"
        )
