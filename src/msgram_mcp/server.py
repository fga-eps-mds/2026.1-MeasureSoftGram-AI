from mcp.server.fastmcp import FastMCP

from tools.ola_mundo import register_tools as register_ola_mundo

mcp_server = FastMCP(
    "MeasureSoftGram",
    host="0.0.0.0",
    port=8000,
    stateless_http=True
)

register_ola_mundo(mcp_server)

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")