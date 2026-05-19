import pytest
import httpx
from unittest.mock import MagicMock

from msgram_mcp.tools.accounts import register_tools


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


def test_buscar_conta_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_conta"]()

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(f"{client.service}accounts/")


def test_buscar_conta_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"id": 1, "username": "admin"}

    result = tools["buscar_conta"]()

    assert result == {"id": 1, "username": "admin"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/accounts/"
    )


def test_buscar_token_acesso_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_detail.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["buscar_token_acesso"]()

    assert exc_info.value.response.status_code == 404
    client.query_detail.assert_called_once_with(
        f"{client.service}accounts/access-token/"
    )


def test_buscar_token_acesso_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_detail.return_value = {"token": "abc123"}

    result = tools["buscar_token_acesso"]()

    assert result == {"token": "abc123"}
    client.query_detail.assert_called_once_with(
        "http://fake-service/api/v1/accounts/access-token/"
    )


def test_listar_repositorios_github_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_repositorios_github"]()

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(
        f"{client.service}accounts/user-repos/"
    )


def test_listar_repositorios_github_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "name": "repo-1"}]

    result = tools["listar_repositorios_github"]()

    assert result == [{"id": 1, "name": "repo-1"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/accounts/user-repos/"
    )


def test_listar_usuarios_erro_404_lanca_excecao(registered_tools):
    tools, client = registered_tools
    request = MagicMock()
    response = MagicMock(status_code=404)
    client.query_list.side_effect = httpx.HTTPStatusError(
        "Not Found", request=request, response=response
    )

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        tools["listar_usuarios"]()

    assert exc_info.value.response.status_code == 404
    client.query_list.assert_called_once_with(f"{client.service}accounts/users/")


def test_listar_usuarios_chama_url_correta(registered_tools):
    tools, client = registered_tools
    client.query_list.return_value = [{"id": 1, "username": "admin"}]

    result = tools["listar_usuarios"]()

    assert result == [{"id": 1, "username": "admin"}]
    client.query_list.assert_called_once_with(
        "http://fake-service/api/v1/accounts/users/"
    )
