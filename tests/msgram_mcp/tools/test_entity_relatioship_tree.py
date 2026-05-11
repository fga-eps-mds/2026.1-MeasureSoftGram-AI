import pytest
import httpx
from unittest.mock import MagicMock, patch

from msgram_mcp.tools.entity_relationship_tree import register_tools


MOCK_RESPONSE = [
    {
        "id": 1,
        "name": "Reliability",
        "key": "reliability",
        "description": None,
        "subcharacteristics": [
            {
                "id": 2,
                "name": "Testing Status",
                "key": "testing_status",
                "description": None,
                "measures": [
                    {"id": 1, "key": "passed_tests", "name": "Passed Tests", "description": None},
                    {"id": 2, "key": "test_builds", "name": "Test Builds", "description": None},
                ],
            }
        ],
    },
    {
        "id": 2,
        "name": "Maintainability",
        "key": "maintainability",
        "description": None,
        "subcharacteristics": [],
    },
]


@pytest.fixture
def listar_arvore_relacionamentos():
    tools = {}

    class CaptureMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn

            return decorator

    register_tools(CaptureMCP(), service="http://fake-service/api/v1/")
    return tools["listar_arvore_relacionamentos"]


@patch("msgram_mcp.tools.entity_relationship_tree.httpx.get")
def test_retorna_lista(mock_get, listar_arvore_relacionamentos):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    result = listar_arvore_relacionamentos()
    assert isinstance(result, list)


@patch("msgram_mcp.tools.entity_relationship_tree.httpx.get")
def test_estrutura_do_item_raiz(mock_get, listar_arvore_relacionamentos):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    item = listar_arvore_relacionamentos()[0]
    assert {"id", "name", "key", "description", "subcharacteristics"} <= item.keys()


@patch("msgram_mcp.tools.entity_relationship_tree.httpx.get")
def test_estrutura_de_subcaracteristica(mock_get, listar_arvore_relacionamentos):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    sub = listar_arvore_relacionamentos()[0]["subcharacteristics"][0]
    assert {"id", "name", "key", "description", "measures"} <= sub.keys()


@patch("msgram_mcp.tools.entity_relationship_tree.httpx.get")
def test_estrutura_de_measure(mock_get, listar_arvore_relacionamentos):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    measure = listar_arvore_relacionamentos()[0]["subcharacteristics"][0]["measures"][0]
    assert {"id", "key", "name", "description"} <= measure.keys()


@patch("msgram_mcp.tools.entity_relationship_tree.httpx.get")
def test_erro_http_lanca_excecao(mock_get, listar_arvore_relacionamentos):
    mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server Error", request=MagicMock(), response=MagicMock()
    )
    with pytest.raises(httpx.HTTPStatusError):
        listar_arvore_relacionamentos()
