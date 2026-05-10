import httpx
from mcp.server.fastmcp import FastMCP

def register_tools(mcp: FastMCP, service: str):

    @mcp.tool()
    def listar_subcaracteristicas() -> list[dict]:
        url = f"{service}supported-subcharacteristics/"
        headers = {
            "accept": "application/json",
            # "authorization": "Basic dGVzdGU6dGVzdGU=",
            # "X-CSRFToken": "nES9z8O1XLfz0arW1CDhk6zGR4miUu29ddoTkpvpdDWz58dDbrPdPLy99ltYN6CG",
        }

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["results"]