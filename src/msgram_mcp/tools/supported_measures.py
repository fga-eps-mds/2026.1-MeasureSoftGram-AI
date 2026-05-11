from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_medidas() -> list[dict]:
        """Lista todas as medidas suportadas pelo MeasureSoftGram."""
        return client.query_list(f"{client.service}supported-measures/", public=True)