from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_metricas() -> list[dict]:
        """Lista todas as métricas suportadas pelo MeasureSoftGram."""
        return client.query_list(f"{client.service}supported-metrics/", public=True)