from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_matriz_balanceamento() -> list[dict]:
        """Lista a matriz de balanceamento entre as entidades do MeasureSoftGram."""
        return client.query_list(f"{client.service}balance-matrix/")
