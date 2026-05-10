from mcp.server.fastmcp import FastMCP

def register_tools(mcp: FastMCP):

    @mcp.tool()
    def ola_mundo() -> str:
        return "Olá mundo!"