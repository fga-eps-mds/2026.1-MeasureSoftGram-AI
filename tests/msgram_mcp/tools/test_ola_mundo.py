from msgram_mcp.tools.ola_mundo import register_tools
from mcp.server.fastmcp import FastMCP

def test_ola_mundo_retorna_string():
    mcp = FastMCP("test")
    register_tools(mcp)

    tool = next(t for t in mcp._tool_manager._tools.values() if t.name == "ola_mundo")
    resultado = tool.fn()

    assert isinstance(resultado, str)
    assert resultado == "Olá mundo!"
