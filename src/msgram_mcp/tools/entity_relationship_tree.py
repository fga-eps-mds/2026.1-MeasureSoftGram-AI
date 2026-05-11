import httpx
from mcp.server.fastmcp import FastMCP


def register_tools(mcp: FastMCP, service: str):

    @mcp.tool()
    def listar_arvore_relacionamentos() -> list[dict]:
        """Lista todas as entidades suportadas pelo MeasureSoftGram e as suas relações no formato de árvore."""
        response = httpx.get(
            f"{service}entity-relationship-tree/",
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            arvore = data
        elif isinstance(data, dict):
            # supports paginated or legacy shape if endpoint changes
            arvore = data.get("results") or data.get("result") or []
        else:
            raise ValueError(f"Formato inesperado da resposta: {type(data).__name__}")

        return arvore
