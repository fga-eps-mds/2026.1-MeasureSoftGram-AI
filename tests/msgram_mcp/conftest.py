import pytest
from mcp.server.fastmcp import FastMCP


@pytest.fixture
def mcp_server():
    server = FastMCP("test-server")
    return server
