import pytest
import httpx
from unittest.mock import MagicMock, patch

from msgram_mcp.auth.msgram_auth import msgram_auth


def make_response(status_code: int, json_data: dict):
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.json.return_value = json_data
    response.raise_for_status = MagicMock()
    if status_code >= 400:
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="error", request=MagicMock(), response=response
        )
    return response


def test_retorna_token_com_credenciais_validas():
    with patch("httpx.post") as mock_post:
        mock_post.return_value = make_response(200, {"key": "fake-token-123"})

        token = msgram_auth(
            service="http://fake/api/v1/", user="admin", password="admin"
        )

    assert token == "fake-token-123"
    mock_post.assert_called_once_with(
        "http://fake/api/v1/accounts/login/",
        json={"username": "admin", "password": "admin"},
        headers={"accept": "application/json"},
    )


def test_credenciais_invalidas_lanca_excecao():
    with patch("httpx.post") as mock_post:
        mock_post.return_value = make_response(
            400, {"non_field_errors": ["credenciais inválidas"]}
        )

        with pytest.raises(httpx.HTTPStatusError):
            msgram_auth(service="http://fake/api/v1/", user="errado", password="errado")
