import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.historical_values import register_tools


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


BASE = "http://fake-service/api/v1/organizations/1/products/2/repositories/3"


def test_listar_historico_caracteristicas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_historico_caracteristicas"](
            organization_pk=1, product_pk=2, repository_pk=3
        )

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/characteristics/"
    )


def test_listar_historico_caracteristicas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "value": 0.75}]

    result = tools["listar_historico_caracteristicas"](
        organization_pk=1, product_pk=2, repository_pk=3
    )

    assert result == [{"id": 1, "value": 0.75}]
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/characteristics/"
    )


def test_buscar_historico_caracteristica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_historico_caracteristica"](
            organization_pk=1, product_pk=2, repository_pk=3, characteristic_id=4
        )

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/characteristics/4/"
    )


def test_buscar_historico_caracteristica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 4, "value": 0.75}

    result = tools["buscar_historico_caracteristica"](
        organization_pk=1, product_pk=2, repository_pk=3, characteristic_id=4
    )

    assert result == {"id": 4, "value": 0.75}
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/characteristics/4/"
    )


def test_listar_historico_subcaracteristicas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_historico_subcaracteristicas"](
            organization_pk=1, product_pk=2, repository_pk=3
        )

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/subcharacteristics/"
    )


def test_listar_historico_subcaracteristicas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "value": 0.6}]

    result = tools["listar_historico_subcaracteristicas"](
        organization_pk=1, product_pk=2, repository_pk=3
    )

    assert result == [{"id": 1, "value": 0.6}]
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/subcharacteristics/"
    )


def test_buscar_historico_subcaracteristica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_historico_subcaracteristica"](
            organization_pk=1, product_pk=2, repository_pk=3, subcharacteristic_id=5
        )

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/subcharacteristics/5/"
    )


def test_buscar_historico_subcaracteristica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 5, "value": 0.6}

    result = tools["buscar_historico_subcaracteristica"](
        organization_pk=1, product_pk=2, repository_pk=3, subcharacteristic_id=5
    )

    assert result == {"id": 5, "value": 0.6}
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/subcharacteristics/5/"
    )


def test_listar_historico_medidas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_historico_medidas"](
            organization_pk=1, product_pk=2, repository_pk=3
        )

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/measures/"
    )


def test_listar_historico_medidas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "value": 0.5}]

    result = tools["listar_historico_medidas"](
        organization_pk=1, product_pk=2, repository_pk=3
    )

    assert result == [{"id": 1, "value": 0.5}]
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/measures/"
    )


def test_buscar_historico_medida_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_historico_medida"](
            organization_pk=1, product_pk=2, repository_pk=3, measure_id=6
        )

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/measures/6/"
    )


def test_buscar_historico_medida_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 6, "value": 0.5}

    result = tools["buscar_historico_medida"](
        organization_pk=1, product_pk=2, repository_pk=3, measure_id=6
    )

    assert result == {"id": 6, "value": 0.5}
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/measures/6/"
    )


def test_listar_historico_metricas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_historico_metricas"](
            organization_pk=1, product_pk=2, repository_pk=3
        )

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/metrics/"
    )


def test_listar_historico_metricas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "value": 85.0}]

    result = tools["listar_historico_metricas"](
        organization_pk=1, product_pk=2, repository_pk=3
    )

    assert result == [{"id": 1, "value": 85.0}]
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/metrics/"
    )


def test_buscar_historico_metrica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_historico_metrica"](
            organization_pk=1, product_pk=2, repository_pk=3, metric_id=7
        )

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/metrics/7/"
    )


def test_buscar_historico_metrica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 7, "value": 85.0}

    result = tools["buscar_historico_metrica"](
        organization_pk=1, product_pk=2, repository_pk=3, metric_id=7
    )

    assert result == {"id": 7, "value": 85.0}
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/metrics/7/"
    )


def test_listar_historico_tsqmi_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_historico_tsqmi"](
            organization_pk=1, product_pk=2, repository_pk=3
        )

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/tsqmi/"
    )


def test_listar_historico_tsqmi_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "value": 0.82}]

    result = tools["listar_historico_tsqmi"](
        organization_pk=1, product_pk=2, repository_pk=3
    )

    assert result == [{"id": 1, "value": 0.82}]
    client.query_list.assert_called_once_with(
        f"{BASE}/historical-values/tsqmi/"
    )


def test_buscar_historico_tsqmi_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_historico_tsqmi"](
            organization_pk=1, product_pk=2, repository_pk=3, tsqmi_id=8
        )

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/tsqmi/8/"
    )


def test_buscar_historico_tsqmi_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 8, "value": 0.82}

    result = tools["buscar_historico_tsqmi"](
        organization_pk=1, product_pk=2, repository_pk=3, tsqmi_id=8
    )

    assert result == {"id": 8, "value": 0.82}
    client.query_detail.assert_called_once_with(
        f"{BASE}/historical-values/tsqmi/8/"
    )
