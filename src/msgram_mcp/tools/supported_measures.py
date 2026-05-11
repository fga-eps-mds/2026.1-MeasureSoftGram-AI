import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str):

    @mcp.tool()
    def listar_medidas() -> list[dict]:
        """Lista todas as medidas suportadas pelo MeasureSoftGram."""
        response = httpx.get(
            f"{service}supported-measures/",
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()["results"]
