from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def buscar_conta() -> dict:
        """Retorna as informações da conta autenticada."""
        return client.query_detail(f"{client.service}accounts/")

    @mcp.tool()
    def buscar_token_acesso() -> dict:
        """Retorna o token de acesso da conta, utilizado em GitHub Actions."""
        return client.query_detail(f"{client.service}accounts/access-token/")

    @mcp.tool()
    def listar_repositorios_github() -> list[dict]:
        """Lista os repositórios do GitHub do usuário autenticado."""
        return client.query_list(f"{client.service}accounts/user-repos/")

    @mcp.tool()
    def listar_usuarios() -> list[dict]:
        """Lista todos os usuários cadastrados no MeasureSoftGram."""
        return client.query_list(f"{client.service}accounts/users/")
