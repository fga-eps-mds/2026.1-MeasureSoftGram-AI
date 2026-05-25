from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def listar_arvore_relacionamentos() -> list[dict]:
        """Lista todas as entidades suportadas pelo MeasureSoftGram e as suas relações no formato de árvore."""
        return client.query_list(
            f"{client.service}entity-relationship-tree/", public=True
        )
