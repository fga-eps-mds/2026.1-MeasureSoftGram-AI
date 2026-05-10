import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str):

    def query(url: str) -> list[dict]:
        response = httpx.get(
            f"{url}",
            headers={
                "accept": "application/json"
            },
        )
        response.raise_for_status()
        return response.json()["results"]

    @mcp.tool()
    def listar_caracteristicas() -> list[dict]:
        """Lista todas as características suportadas pelo MeasureSoftGram."""
        return query(f"{service}supported-characteristics/")


    @mcp.tool()
    def listar_subcaracteristicas() -> list[dict]:
        """Lista todas as subcaracterísticas suportadas pelo MeasureSoftGram."""
        return query(f"{service}supported-subcharacteristics/")
