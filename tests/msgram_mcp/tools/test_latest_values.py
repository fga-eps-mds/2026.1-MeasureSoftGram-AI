import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.latest_values import register_tools


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


# --- características ---

def test_listar_ultimas_caracteristicas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "name": "reliability"}]

    result = tools["listar_ultimas_caracteristicas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == [{"id": 1, "name": "reliability"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/characteristics/"
    )


def test_listar_ultimas_caracteristicas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_ultimas_caracteristicas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404


def test_buscar_ultima_caracteristica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 5, "name": "reliability", "value": 0.9}

    result = tools["buscar_ultima_caracteristica"](
        organization_pk=1, product_pk=2, repository_pk=3, characteristic_id=5
    )

    assert result == {"id": 5, "name": "reliability", "value": 0.9}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/characteristics/5/"
    )


def test_buscar_ultima_caracteristica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_ultima_caracteristica"](
            organization_pk=1, product_pk=2, repository_pk=3, characteristic_id=99
        )

    assert exc_info.value.response.status_code == 404


# --- subcaracterísticas ---

def test_listar_ultimas_subcaracteristicas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 2, "name": "testing"}]

    result = tools["listar_ultimas_subcaracteristicas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == [{"id": 2, "name": "testing"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/subcharacteristics/"
    )


def test_listar_ultimas_subcaracteristicas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_ultimas_subcaracteristicas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404


def test_buscar_ultima_subcaracteristica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 7, "name": "testing", "value": 0.75}

    result = tools["buscar_ultima_subcaracteristica"](
        organization_pk=1, product_pk=2, repository_pk=3, subcharacteristic_id=7
    )

    assert result == {"id": 7, "name": "testing", "value": 0.75}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/subcharacteristics/7/"
    )


def test_buscar_ultima_subcaracteristica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_ultima_subcaracteristica"](
            organization_pk=1, product_pk=2, repository_pk=3, subcharacteristic_id=99
        )

    assert exc_info.value.response.status_code == 404


# --- medidas ---

def test_listar_ultimas_medidas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "name": "test_coverage"}]

    result = tools["listar_ultimas_medidas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == [{"id": 1, "name": "test_coverage"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/measures/"
    )


def test_listar_ultimas_medidas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_ultimas_medidas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404


def test_buscar_ultima_medida_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 4, "name": "test_coverage", "value": 0.8}

    result = tools["buscar_ultima_medida"](
        organization_pk=1, product_pk=2, repository_pk=3, measure_id=4
    )

    assert result == {"id": 4, "name": "test_coverage", "value": 0.8}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/measures/4/"
    )


def test_buscar_ultima_medida_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_ultima_medida"](
            organization_pk=1, product_pk=2, repository_pk=3, measure_id=99
        )

    assert exc_info.value.response.status_code == 404


# --- métricas ---

def test_listar_ultimas_metricas_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "name": "coverage"}]

    result = tools["listar_ultimas_metricas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == [{"id": 1, "name": "coverage"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/metrics/"
    )


def test_listar_ultimas_metricas_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_ultimas_metricas"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404


def test_buscar_ultima_metrica_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 6, "name": "coverage", "value": 0.95}

    result = tools["buscar_ultima_metrica"](
        organization_pk=1, product_pk=2, repository_pk=3, metric_id=6
    )

    assert result == {"id": 6, "name": "coverage", "value": 0.95}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/metrics/6/"
    )


def test_buscar_ultima_metrica_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_ultima_metrica"](
            organization_pk=1, product_pk=2, repository_pk=3, metric_id=99
        )

    assert exc_info.value.response.status_code == 404


# --- tsqmi ---

def test_listar_ultimo_tsqmi_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"value": 0.88}]

    result = tools["listar_ultimo_tsqmi"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == [{"value": 0.88}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/tsqmi/"
    )


def test_listar_ultimo_tsqmi_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_ultimo_tsqmi"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404


def test_buscar_badge_tsqmi_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"badge": "A", "value": 0.88}

    result = tools["buscar_badge_tsqmi"](organization_pk=1, product_pk=2, repository_pk=3)

    assert result == {"badge": "A", "value": 0.88}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/organizations/1/products/2/repositories/3/latest-values/tsqmi/badge/"
    )


def test_buscar_badge_tsqmi_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_badge_tsqmi"](organization_pk=1, product_pk=2, repository_pk=3)

    assert exc_info.value.response.status_code == 404
