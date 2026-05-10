import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str):

    @mcp.tool()
    def listar_subcaracteristicas() -> list[dict]:
        """Lista todas as subcaracterísticas suportadas pelo MeasureSoftGram."""
        response = httpx.get(
            f"{service}supported-subcharacteristics/",
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()["results"]
