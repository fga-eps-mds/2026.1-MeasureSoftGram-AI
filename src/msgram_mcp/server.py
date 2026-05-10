import os

from mcp.server.fastmcp import FastMCP
from msgram_mcp.tools.supported_characteristics import register_tools

SERVICE = os.getenv("SERVICE")
if not SERVICE:
    raise ValueError("Variável de ambiente SERVICE não configurada")

mcp_server = FastMCP("MeasureSoftGram", host="0.0.0.0", port=8000, stateless_http=True)

register_tools(mcp_server, service=SERVICE)

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
