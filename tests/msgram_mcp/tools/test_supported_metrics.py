import pytest
import httpx
from unittest.mock import MagicMock
from msgram_mcp.tools.supported_metrics import register_tools


@pytest.fixture
def listar_metricas():
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
    return tools["listar_metricas"], client

def test_erro_404_lanca_excecao(listar_metricas):
    fn, client = listar_metricas

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
        f"{client.service}supported-metrics/",
        public=True,
    )


def test_retorno_sucesso_lista_metricas(listar_metricas):
    fn, client = listar_metricas

    expected = [
        {"id": 1, "key": "coverage", "name": "Coverage", "description": None},
        {"id": 2, "key": "complexity", "name": "Complexity", "description": None},
    ]
    client.query_list.return_value = expected

    result = fn()

    assert result == expected
    assert isinstance(result, list)
    client.query_list.assert_called_once_with(
        f"{client.service}supported-metrics/",
        public=True,
    )

