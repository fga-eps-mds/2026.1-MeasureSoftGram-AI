import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.supported_characteristics import register_tools


@pytest.fixture
def listar_caracteristicas():
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
    return tools["listar_caracteristicas"], client


@pytest.fixture
def listar_subcaracteristicas():
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
    return tools["listar_subcaracteristicas"], client


def test_listar_caracteristicas_erro_404_lanca_excecao(listar_caracteristicas):
    fn, client = listar_caracteristicas

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        fn()

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}supported-characteristics/",
        public=True,
    )


def test_listar_subcaracteristicas_erro_404_lanca_excecao(listar_subcaracteristicas):
    fn, client = listar_subcaracteristicas

    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found",
        request=request,
        response=response,
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        fn()

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}supported-subcharacteristics/",
        public=True,
    )


def test_listar_caracteristicas_retorno_sucesso_lista(listar_caracteristicas):
    fn, client = listar_caracteristicas

    expected = [
        {"id": 1, "key": "reliability", "name": "Reliability", "description": None},
        {"id": 2, "key": "maintainability", "name": "Maintainability", "description": None},
    ]
    client.query_list.return_value = expected

    result = fn()

    assert result == expected
    assert isinstance(result, list)
    client.query_list.assert_called_once_with(
        f"{client.service}supported-characteristics/",
        public=True,
    )


def test_listar_subcaracteristicas_retorno_sucesso_lista(listar_subcaracteristicas):
    fn, client = listar_subcaracteristicas

    expected = [
        {"id": 1, "key": "testing_status", "name": "Testing Status", "description": None},
        {"id": 2, "key": "maturity", "name": "Maturity", "description": None},
    ]
    client.query_list.return_value = expected

    result = fn()

    assert result == expected
    assert isinstance(result, list)
    client.query_list.assert_called_once_with(
        f"{client.service}supported-subcharacteristics/",
        public=True,
    )

