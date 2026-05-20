import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.repositories import register_tools


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


def test_listar_repositorios_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "name": "repo-1"}]

    result = tools["listar_repositorios"](organization_pk=1, product_pk=2)

    assert result == [{"id": 1, "name": "repo-1"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/"
    )


def test_listar_repositorios_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_repositorios"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/"
    )


def test_buscar_repositorio_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 3, "name": "repo-3"}

    result = tools["buscar_repositorio"](organization_pk=1, product_pk=2, repository_id=3)

    assert result == {"id": 3, "name": "repo-3"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/"
    )


def test_buscar_repositorio_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_repositorio"](organization_pk=1, product_pk=2, repository_id=99)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/99/"
    )


def test_buscar_arvore_relacionamentos_produto_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"entity": "characteristic", "children": []}]

    result = tools["buscar_arvore_relacionamentos_produto"](organization_pk=1, product_pk=2)

    assert result == [{"entity": "characteristic", "children": []}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/entity-relationship-tree/"
    )


def test_buscar_arvore_relacionamentos_produto_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_arvore_relacionamentos_produto"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404


def test_listar_tsqmi_historico_repositorios_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"date": "2024-01-01", "value": 0.85}]

    result = tools["listar_tsqmi_historico_repositorios"](organization_pk=1, product_pk=2)

    assert result == [{"date": "2024-01-01", "value": 0.85}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories-tsqmi-historical-values/"
    )


def test_listar_tsqmi_historico_repositorios_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_tsqmi_historico_repositorios"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404


def test_listar_tsqmi_recente_repositorios_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"repository": "repo-1", "value": 0.90}]

    result = tools["listar_tsqmi_recente_repositorios"](organization_pk=1, product_pk=2)

    assert result == [{"repository": "repo-1", "value": 0.90}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories-tsqmi-latest-values/"
    )


def test_listar_tsqmi_recente_repositorios_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_tsqmi_recente_repositorios"](organization_pk=1, product_pk=2)

    assert exc_info.value.response.status_code == 404
