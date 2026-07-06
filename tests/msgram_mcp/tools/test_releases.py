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


def test_buscar_release_config_atual_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 1, "config": "release-config"}

    result = tools["buscar_release_config_atual"](organization_pk=1, product_pk=2)

    assert result == {"id": 1, "config": "release-config"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/current/release-config/"
    )


def test_listar_releases_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1}, {"id": 2}]

    result = tools["listar_releases"](organization_pk=1, product_pk=2)

    assert result == [{"id": 1}, {"id": 2}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/"
    )


def test_verificar_release_valido_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"is_valid": True}

    result = tools["verificar_release_valido"](organization_pk=1, product_pk=2)

    assert result == {"is_valid": True}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/is-valid/"
    )


def test_buscar_release_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 3, "name": "release-1"}

    result = tools["buscar_release"](organization_pk=1, product_pk=2, release_id=3)

    assert result == {"id": 3, "name": "release-1"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/3/"
    )


def test_buscar_analysis_data_release_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"metric": "value"}

    result = tools["buscar_analysis_data_release"](
        organization_pk=1, product_pk=2, release_id=3
    )

    assert result == {"metric": "value"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/3/analysis_data/"
    )


def test_buscar_planned_x_accomplished_chama_url_correta_e_trata_dados(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {
        "planned": [80, 70, 90],
        "accomplished": [75, 70, 95],
    }

    result = tools["buscar_planned_x_accomplished"](
        organization_pk=1, product_pk=2, release_id=3
    )

    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/3/planeed-x-accomplished/"
    )

    assert result["raw"] == {
        "planned": [80, 70, 90],
        "accomplished": [75, 70, 95],
    }
    assert result["treatment_error"] is None
    assert result["characteristics"] == [
        {
            "name": "Reliability",
            "planned": 80,
            "accomplished": 75,
            "diff": 5,
            "norm_diff": 5,
        },
        {
            "name": "Maintainability",
            "planned": 70,
            "accomplished": 70,
            "diff": 0,
            "norm_diff": 0,
        },
        {
            "name": "Functional Suitability",
            "planned": 90,
            "accomplished": 95,
            "diff": -5,
            "norm_diff": 0,
        },
    ]


def test_buscar_planned_x_accomplished_erro_no_tratamento_retorna_raw_com_erro(
    registered_tools,
):
    tools, client = registered_tools
    client.query_detail.return_value = {"unexpected": "shape"}

    result = tools["buscar_planned_x_accomplished"](
        organization_pk=1, product_pk=2, release_id=3
    )

    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/release/3/planeed-x-accomplished/"
    )

    assert result["raw"] == {"unexpected": "shape"}
    assert result["characteristics"] is None
    assert result["treatment_error"] is not None