import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.goals import register_tools


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


def test_listar_todos_objetivos_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_todos_objetivos"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}organizations/1/products/2/all/goal/"
    )


def test_listar_todos_objetivos_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "goal": "improve coverage"}]

    result = tools["listar_todos_objetivos"](organization_pk=1, product_pk=2)

    assert result == [{"id": 1, "goal": "improve coverage"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/all/goal/"
    )


def test_buscar_objetivo_atual_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_objetivo_atual"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/1/products/2/current/goal/"
    )


def test_buscar_objetivo_atual_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 1, "goal": "current goal"}

    result = tools["buscar_objetivo_atual"](organization_pk=1, product_pk=2)

    assert result == {"id": 1, "goal": "current goal"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/current/goal/"
    )


def test_buscar_pre_config_padrao_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_pre_config_padrao"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/1/products/2/default/pre-config/"
    )


def test_buscar_pre_config_padrao_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 1, "config": "default"}

    result = tools["buscar_pre_config_padrao"](organization_pk=1, product_pk=2)

    assert result == {"id": 1, "config": "default"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/default/pre-config/"
    )
