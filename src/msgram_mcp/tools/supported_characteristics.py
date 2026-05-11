from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_caracteristicas() -> list[dict]:
        """Lista todas as características suportadas pelo MeasureSoftGram."""
        return client.query_list(f"{client.service}supported-characteristics/", public=True)

    @mcp.tool()
    def listar_subcaracteristicas() -> list[dict]:
        """Lista todas as subcaracterísticas suportadas pelo MeasureSoftGram."""
        return client.query_list(f"{client.service}supported-subcharacteristics/", public=True)