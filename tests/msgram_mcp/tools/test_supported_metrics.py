import pytest
import httpx
from unittest.mock import MagicMock, patch
from msgram_mcp.tools.supported_metrics import register_tools

MOCK_RESPONSE = {
    "count": 17,
    "next": None,
    "previous": None,
        "results": [
            {
                "id": 12,
                "key": "comment_lines_density",
                "name": "Comments (%)",
                "description": None
            },
            {
                "id": 8,
                "key": "complexity",
                "name": "Cyclomatic Complexity",
                "description": None
            },
            {
                "id": 10,
                "key": "coverage",
                "name": "Coverage",
                "description": None
            },
            {
                "id": 14,
                "key": "duplicated_lines_density",
                "name": "Duplicated lines density",
                "description": None
            },
            {
                "id": 7,
                "key": "files",
                "name": "Files",
                "description": None
            },
            {
                "id": 1,
                "key": "functions",
                "name": "number of functions",
                "description": None
            },
            {
                "id": 9,
                "key": "ncloc",
                "name": "Lines of Code",
                "description": None
            },
            {
                "id": 11,
                "key": "reliability_rating",
                "name": "Reliabiity Rating",
                "description": None
            },
            {
                "id": 17,
                "key": "resolved_issues",
                "name": "Resolved issues",
                "description": None
            },
            {
                "id": 5,
                "key": "security_rating",
                "name": "rating of security",
                "description": None
            },
            {
                "id": 15,
                "key": "sum_ci_feedback_times",
                "name": "Sum of time in seconds on builds",
                "description": None
            },
            {
                "id": 4,
                "key": "test_errors",
                "name": "number of tests errors",
                "description": None
            },
            {
                "id": 2,
                "key": "test_execution_time",
                "name": "average time to execute tests",
                "description": None
            },
            {
                "id": 3,
                "key": "test_failures",
                "name": "number of tests failuress",
                "description": None
            },
            {
                "id": 13,
                "key": "test_success_density",
                "name": "Test Success Density",
                "description": None
            },
            {
                "id": 6,
                "key": "tests",
                "name": "Tests",
                "description": None
            },
            {
                "id": 16,
                "key": "total_builds",
                "name": "Total build count",
                "description": None
            },
            {
                "id": 18,
                "key": "total_issues",
                "name": "Total issues",
                "description": None
            }
        ],
}


@pytest.fixture
def listar_metricas():
    tools = {}

    class CaptureMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn

            return decorator

    register_tools(CaptureMCP(), service="http://fake-service/api/v1/")
    return tools["listar_metricas"]


@patch("msgram_mcp.tools.supported_metrics.httpx.get")
def test_retorna_lista(mock_get, listar_metricas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    assert isinstance(listar_metricas(), list)


@patch("msgram_mcp.tools.supported_metrics.httpx.get")
def test_estrutura_do_item(mock_get, listar_metricas):
    mock_get.return_value.json.return_value = MOCK_RESPONSE
    item = listar_metricas()[0]
    assert {"id", "key", "name", "description"} <= item.keys()


@patch("msgram_mcp.tools.supported_metrics.httpx.get")
def test_erro_http_lanca_excecao(mock_get, listar_metricas):
    mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Server Error", request=MagicMock(), response=MagicMock()
    )
    with pytest.raises(httpx.HTTPStatusError):
        listar_metricas()
