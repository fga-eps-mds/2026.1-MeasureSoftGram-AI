import pytest
import httpx
from unittest.mock import MagicMock, patch
from msgram_mcp.tools.supported_measures import register_tools

MOCK_RESPONSE = {
    "count": 8,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": 1,
            "key": "passed_tests",
            "name": "Passed Tests",
            "description": None
        },
        {
            "id": 2,
            "key": "test_builds",
            "name": "Test Builds",
            "description": None
        },
        {
            "id": 3,
            "key": "test_coverage",
            "name": "Test Coverage",
            "description": None
        },
        {
            "id": 4,
            "key": "non_complex_file_density",
            "name": "Non Complex File Density",
            "description": None
        },
        {
            "id": 5,
            "key": "commented_file_density",
            "name": "Commented File Density",
            "description": None
        },
        {
            "id": 6,
            "key": "duplication_absense",
            "name": "Duplication Absense",
            "description": None
        },
        {
            "id": 7,
            "key": "team_throughput",
            "name": "Team Throughput",
            "description": None
        },
        {
            "id": 8,
            "key": "ci_feedback_time",
            "name": "Ci Feedback Time",
            "description": None
        }
    ]
}


@pytest.fixture
def listar_medidas():
    tools = {}

    class CaptureMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn

            return decorator

    register_tools(CaptureMCP(), service="http://fake-service/api/v1/")
    return tools["listar_medidas"]


@patch("msgram_mcp.tools.supported_measures.httpx.get")
def test_retorna_lista(mock_get, listar_medidas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    assert isinstance(listar_medidas(), list)


@patch("msgram_mcp.tools.supported_measures.httpx.get")
def test_estrutura_do_item(mock_get, listar_medidas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    item = listar_medidas()[0]
    assert {"id", "key", "name", "description"} <= item.keys()


@patch("msgram_mcp.tools.supported_measures.httpx.get")
def test_erro_http_lanca_excecao(mock_get, listar_medidas):
    mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server Error", request=MagicMock(), response=MagicMock()
    )
    with pytest.raises(httpx.HTTPStatusError):
        listar_medidas()
