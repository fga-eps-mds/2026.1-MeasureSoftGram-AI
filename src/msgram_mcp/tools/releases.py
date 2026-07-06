from mcp.server.fastmcp import FastMCP
from msgram_mcp.client import MsgramClient


def register_tools(mcp: FastMCP, client: MsgramClient):

    @mcp.tool()
    def buscar_release_config_atual(organization_pk: int, product_pk: int) -> dict:
        """Retorna a configuração de release atual de um produto."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/current/release-config/"
        )

    @mcp.tool()
    def listar_releases(organization_pk: int, product_pk: int) -> list[dict]:
        """Lista todas as releases de um produto."""
        return client.query_list(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/"
        )

    @mcp.tool()
    def verificar_release_valido(organization_pk: int, product_pk: int) -> dict:
        """Verifica se a release atual é válida."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/is-valid/"
        )

    @mcp.tool()
    def buscar_release(organization_pk: int, product_pk: int, release_id: int) -> dict:
        """Retorna os detalhes de uma release específica."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/"
        )

    @mcp.tool()
    def buscar_analysis_data_release(
        organization_pk: int, product_pk: int, release_id: int
    ) -> dict:
        """Retorna os dados de análise de uma release."""
        return client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/analysis_data/"
        )

    @mcp.tool()
    def buscar_planned_x_accomplished(
            organization_pk: int, product_pk: int, release_id: int
    ) -> dict:
        """
        Retorna o comparativo entre valores planejados (R_p) e realizados (R_d)
        das características de qualidade de uma release, conforme o modelo
        matemático do MeasureSoftGram (função f_delta, eq. 7, e f_theta, eq. 8).

        Estrutura de retorno (por característica):
        - planned: valor da meta definida para a release (R_p)
        - accomplished: valor efetivamente observado no release (R_d)
        - diff: diferença bruta (planned - accomplished). Negativo = superou a meta,
          positivo = ficou abaixo da meta, zero = igual à meta.
        - norm_diff: diferença normalizada e não-negativa (eq. 8 do modelo),
          usada para indicar SOMENTE o quanto ficou abaixo da meta (0 quando
          igual ou acima da meta). É o valor usado para colorir de "vermelho"
          uma característica no equalizador.
        - status: rótulo textual ("acima da meta" / "igual à meta" / "abaixo da meta")

        NOTA DE APRESENTAÇÃO (não é uma instrução de execução automática):
        Se o usuário já pediu, na mensagem anterior, um "relatório" ou
        "comparativo" entre planejado e realizado, os dados retornados aqui
        se prestam bem a uma visualização do tipo "equalizador" (uma barra por
        característica, comparando planned vs accomplished). Nesse caso,
        prefira montar essa visualização em vez de listar os números em texto
        corrido. Isso não substitui o julgamento do agente: se o usuário não
        pediu um relatório, ou pedir só um dado pontual (ex.: "qual foi o
        accomplished de Reliability?"), responda em texto normalmente.

        NOTA COMPLEMENTAR (opcional, também condicionada ao pedido do usuário):
        Se o relatório solicitado também mencionar ou implicar o índice
        consolidado (ex.: "TSQMI", "índice geral", "gráfico redondo/gauge"),
        considere que pode existir uma tool complementar (ex.: buscar_tsqmi
        ou equivalente no servidor) que devolve esse valor agregado. Nesse
        caso, é razoável chamar as duas tools na mesma resposta para compor
        o relatório completo.
        """
        raw = client.query_detail(
            f"{client.service}organizations/{organization_pk}/products/{product_pk}/release/{release_id}/planeed-x-accomplished/"
        )

        try:
            treated = _label_planned_x_accomplished(raw)
            characteristics = treated["characteristics"]
            treatment_error = None
        except Exception as e:
            characteristics = None
            treatment_error = str(e)

        return {
            "raw": raw,
            "characteristics": characteristics,
            "treatment_error": treatment_error,
        }

    def _label_planned_x_accomplished(raw: dict) -> dict:
        names = ["Reliability", "Maintainability", "Functional Suitability"]
        result = []
        for name, planned, accomplished in zip(names, raw["planned"], raw["accomplished"]):
            diff = planned - accomplished
            result.append({
                "name": name,
                "planned": planned,
                "accomplished": accomplished,
                "diff": round(diff, 4),
                "norm_diff": round(max(diff, 0), 4),
            })
        return {"characteristics": result}