import os
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP
from msgram_mcp.tools.supported_characteristics import register_tools as supported_characteristics
from msgram_mcp.tools.organizations import register_tools as organization_register
from msgram_mcp.tools.supported_metrics import register_tools as register_metrics_tools
from msgram_mcp.auth.msgram_auth import msgram_auth


@dataclass(frozen=True)
class Settings:
    service: str
    token: str

    @classmethod
    def from_env(cls) -> "Settings":
        missing = [var for var in ("SERVICE", "MSGRAM_USER", "MSGRAM_PASSWORD") if not os.getenv(var)]
        if missing:
            raise ValueError(f"Variáveis de ambiente não configuradas: {', '.join(missing)}")

        service = os.getenv("SERVICE")
        token = msgram_auth(service=service, user=os.getenv("MSGRAM_USER"), password=os.getenv("MSGRAM_PASSWORD"))

        return cls(
            service=service,
            token=token,
        )


def create_server(settings: Settings) -> FastMCP:
    mcp_server = FastMCP("MeasureSoftGram", host="0.0.0.0", port=8000, stateless_http=True)

    supported_characteristics(mcp_server, service=settings.service)
    organization_register(mcp_server, service=settings.service, token=settings.token)
    register_metrics_tools(mcp_server, service=settings.service)

    return mcp_server


settings = Settings.from_env()
mcp_server = create_server(settings)

if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")