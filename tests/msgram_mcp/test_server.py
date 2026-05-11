from unittest.mock import patch

import pytest

from msgram_mcp.server import Settings, create_server


class TestSettings:
    def test_from_env_retorna_settings_correto(self):
        envs = {
            "SERVICE": "http://test/api/v1/",
            "MSGRAM_USER": "admin",
            "MSGRAM_PASSWORD": "admin",
        }
        with patch.dict("os.environ", envs):
            with patch(
                "msgram_mcp.server.msgram_auth", return_value="fake-token"
            ) as mock_auth:
                settings = Settings.from_env()

        assert settings.service == "http://test/api/v1/"
        assert settings.token == "fake-token"
        mock_auth.assert_called_once_with(
            service="http://test/api/v1/", user="admin", password="admin"
        )

    def test_from_env_levanta_erro_com_envs_faltando(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc:
                Settings.from_env()

        assert "SERVICE" in str(exc.value)
        assert "MSGRAM_USER" in str(exc.value)
        assert "MSGRAM_PASSWORD" in str(exc.value)

    def test_from_env_levanta_erro_somente_com_env_faltando(self):
        envs = {"SERVICE": "http://test/api/v1/", "MSGRAM_USER": "admin"}
        with patch.dict("os.environ", envs, clear=True):
            with pytest.raises(ValueError) as exc:
                Settings.from_env()

        assert "MSGRAM_PASSWORD" in str(exc.value)
        assert "SERVICE" not in str(exc.value)


class TestCreateServer:
    def test_create_server_passa_client_correto_para_tools(self):
        settings = Settings(service="http://test/api/v1/", token="fake-token")

        with patch("msgram_mcp.server.supported_characteristics_tools") as mock_tool:
            with patch("msgram_mcp.server.organization_register_tools"):
                with patch("msgram_mcp.server.register_metrics_tools"):
                    with patch("msgram_mcp.server.releases_tools"):
                        with patch("msgram_mcp.server.register_measures_tools"):
                            with patch(
                                "msgram_mcp.server.entity_relationship_tree_tools"
                            ):
                                create_server(settings)

        _, kwargs = mock_tool.call_args
        assert kwargs["client"].service == "http://test/api/v1/"
