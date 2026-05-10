import pytest
import httpx
from unittest.mock import MagicMock, patch
from msgram_mcp.tools.supported_characteristics import register_tools

MOCK_RESPONSE = {
    "count": 4,
    "next": None,
    "previous": None,
    "results": [
        {"id": 1, "key": "modifiability", "name": "Modifiability", "description": None},
        {
            "id": 2,
            "key": "testing_status",
            "name": "Testing Status",
            "description": None,
        },
        {
            "id": 3,
            "key": "functional_completeness",
            "name": "Functional Completeness",
            "description": None,
        },
        {"id": 4, "key": "maturity", "name": "Maturity", "description": None},
    ],
}


@pytest.fixture
def listar_subcaracteristicas():
    tools = {}

    class CaptureMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn

            return decorator

    register_tools(CaptureMCP(), service="http://fake-service/api/v1/")
    return tools["listar_subcaracteristicas"]


@patch("msgram_mcp.tools.supported_characteristics.httpx.get")
def test_retorna_lista(mock_get, listar_subcaracteristicas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    assert isinstance(listar_subcaracteristicas(), list)


@patch("msgram_mcp.tools.supported_characteristics.httpx.get")
def test_estrutura_do_item(mock_get, listar_subcaracteristicas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    item = listar_subcaracteristicas()[0]
    assert {"id", "key", "name", "description"} <= item.keys()


@patch("msgram_mcp.tools.supported_characteristics.httpx.get")
def test_erro_http_lanca_excecao(mock_get, listar_subcaracteristicas):
    mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server Error", request=MagicMock(), response=MagicMock()
    )
    with pytest.raises(httpx.HTTPStatusError):
        listar_subcaracteristicas()
