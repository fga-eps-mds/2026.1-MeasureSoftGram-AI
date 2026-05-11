import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.releases import register_tools


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

def test_buscar_release_config_atual_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_release_config_atual"](organization_pk, product_pk)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/current/release-config/"
    )

def test_listar_releases_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_releases"](organization_pk, product_pk)

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/"
    )

def test_verificar_release_valido_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["verificar_release_valido"](organization_pk, product_pk)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/is-valid/"
    )

def test_buscar_release_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2
    release_id = 3

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_release"](organization_pk, product_pk, release_id)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/"
    )

def test_buscar_analysis_data_release_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2
    release_id = 3

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_analysis_data_release"](organization_pk, product_pk, release_id)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/analysis_data/"
    )

def test_buscar_planned_x_accomplished_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)

    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    organization_pk = 1
    product_pk = 2
    release_id = 3

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_planned_x_accomplished"](organization_pk, product_pk, release_id)

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/planeed-x-accomplished/"
    )
