from unittest.mock import MagicMock, patch

import httpx
import pytest

from msgram_mcp.client import MsgramClient


@pytest.fixture
def client():
    return MsgramClient(service="http://test/api/v1/", token="fake-token")


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


class TestMsgramClientHeaders:
    def test_auth_headers_contém_authorization(self, client):
        assert "Authorization" in client._auth_headers
        assert client._auth_headers["Authorization"] == "Token fake-token"

    def test_public_headers_nao_contém_authorization(self, client):
        assert "Authorization" not in client._public_headers

    def test_get_usa_auth_headers_por_padrao(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(200, {})
            client._get("http://test/api/v1/organizations/")
            mock_get.assert_called_once_with(
                "http://test/api/v1/organizations/", headers=client._auth_headers
            )

    def test_get_usa_public_headers_quando_solicitado(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(200, {})
            client._get("http://test/api/v1/supported-metrics/", public=True)
            mock_get.assert_called_once_with(
                "http://test/api/v1/supported-metrics/", headers=client._public_headers
            )


class TestMsgramClientQueryList:
    def test_retorna_results_quando_presente(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(
                200, {"results": [{"id": 1}], "count": 1}
            )
            result = client.query_list("http://test/api/v1/organizations/")
            assert result == [{"id": 1}]

    def test_retorna_data_diretamente_quando_sem_results(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(200, [{"id": 1}, {"id": 2}])
            result = client.query_list("http://test/api/v1/entity-relationship-tree/")
            assert result == [{"id": 1}, {"id": 2}]


class TestMsgramClientQueryDetail:
    def test_retorna_dict_do_objeto(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(200, {"id": 1, "name": "fga-eps-mds"})
            result = client.query_detail("http://test/api/v1/organizations/1/")
            assert result == {"id": 1, "name": "fga-eps-mds"}


class TestMsgramClientErros:
    def test_levanta_runtime_error_em_500(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(500, {})
            with pytest.raises(RuntimeError, match="Erro interno no servidor."):
                client._get("http://test/api/v1/organizations/")

    def test_levanta_http_error_em_404(self, client):
        with patch("httpx.get") as mock_get:
            mock_get.return_value = make_response(404, {})
            with pytest.raises(httpx.HTTPStatusError):
                client._get("http://test/api/v1/organizations/999/")
