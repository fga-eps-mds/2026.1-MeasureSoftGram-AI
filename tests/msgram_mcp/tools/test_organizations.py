import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.organizations import register_tools


@pytest.fixture
def registered_tools():
    tools = {}

    class CaptureMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn

            return decorator

    client = MagicMock()
    client.service = "http://fake-service/api/v1/"

    register_tools(CaptureMCP(), client=client)
    return tools, client

def test_listar_organizacoes_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_organizacoes"]()

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(f"{client.service}organizations/")

def test_buscar_organizacao_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    org_id = 10
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_organizacao"](org_id)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(f"{client.service}organizations/{org_id}/")

def test_listar_produtos_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    org_id = 20
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_produtos"](org_id)

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}organizations/{org_id}/products/"
    )

def test_buscar_produto_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    org_id = 30
    product_id = 7
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_produto"](org_id, product_id)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{org_id}/products/{product_id}/"
    )
