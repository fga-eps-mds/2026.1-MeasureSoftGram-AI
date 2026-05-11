import pytest
import httpx
from unittest.mock import MagicMock, patch
from msgram_mcp.tools.supported_measures import register_tools


@pytest.fixture
def listar_medidas():
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
    return tools["listar_medidas"], client

def test_erro_404_lanca_excecao(listar_medidas):
    fn, client = listar_medidas

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
        f"{client.service}supported-measures/",
        public=True,
    )
