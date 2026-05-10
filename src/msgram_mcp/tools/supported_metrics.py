import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str):

    @mcp.tool()
    def listar_metricas() -> list[dict]:
        """Lista todas as métricas suportadas pelo MeasureSoftGram."""
        response = httpx.get(
            f"{service}supported-metrics/",
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()["results"]
