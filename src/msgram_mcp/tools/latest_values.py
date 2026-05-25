from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_ultimas_caracteristicas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o último valor calculado de cada característica de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/characteristics/"
        )

    @mcp.tool()
    def buscar_ultima_caracteristica(
        organization_pk: int, product_pk: int, repository_pk: int, characteristic_id: int
    ) -> dict:
        """Retorna o último valor calculado de uma característica específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/characteristics/{characteristic_id}/"
        )

    @mcp.tool()
    def listar_ultimas_subcaracteristicas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o último valor calculado de cada subcaracterística de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/subcharacteristics/"
        )

    @mcp.tool()
    def buscar_ultima_subcaracteristica(
        organization_pk: int, product_pk: int, repository_pk: int, subcharacteristic_id: int
    ) -> dict:
        """Retorna o último valor calculado de uma subcaracterística específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/subcharacteristics/{subcharacteristic_id}/"
        )

    @mcp.tool()
    def listar_ultimas_medidas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o último valor coletado de cada medida de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/measures/"
        )

    @mcp.tool()
    def buscar_ultima_medida(
        organization_pk: int, product_pk: int, repository_pk: int, measure_id: int
    ) -> dict:
        """Retorna o último valor coletado de uma medida específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/measures/{measure_id}/"
        )

    @mcp.tool()
    def listar_ultimas_metricas(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o último valor coletado de cada métrica de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/metrics/"
        )

    @mcp.tool()
    def buscar_ultima_metrica(
        organization_pk: int, product_pk: int, repository_pk: int, metric_id: int
    ) -> dict:
        """Retorna o último valor coletado de uma métrica específica de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/metrics/{metric_id}/"
        )

    @mcp.tool()
    def listar_ultimo_tsqmi(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> list[dict]:
        """Lista o último valor de TSQMI de um repositório."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/tsqmi/"
        )

    @mcp.tool()
    def buscar_badge_tsqmi(
        organization_pk: int, product_pk: int, repository_pk: int
    ) -> dict:
        """Retorna o badge de TSQMI de um repositório."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/repositories/{repository_pk}/latest-values/tsqmi/badge/"
        )
