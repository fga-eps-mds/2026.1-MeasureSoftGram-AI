# MeasureSoftGram AI

Servidor MCP (Model Context Protocol) que expõe os dados do MeasureSoftGram como ferramentas para modelos de linguagem (LLMs).

## O que é possível fazer

Com esse MCP conectado, um LLM consegue:

- Listar organizações, produtos e releases cadastrados
- Consultar características, subcaracterísticas, métricas e medidas suportadas
- Verificar configurações e status de releases
- Acessar dados de análise e comparativos entre planejado e realizado
- Navegar pela árvore de relacionamentos entre entidades do MeasureSoftGram

## Como vincular a sua IA?

Basta adicionar o MCP do seu agente através do comando enquanto roda o projeto localmente:

```json
{
  "mcpServers": {
    "measuresoftgram": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

---

## Estrutura de pastas

```txt
src/msgram_mcp/
├── __init__.py
├── server.py               # ponto de entrada — sobe o FastMCP e registra as tools
├── client.py               # cliente HTTP compartilhado entre as tools
├── auth/
│   └── msgram_auth.py      # autenticação com o msgram-service
└── tools/
    ├── __init__.py
    ├── organizations.py
    ├── releases.py
    ├── supported_characteristics.py
    ├── supported_measures.py
    ├── supported_metrics.py
    └── entity_relationship_tree.py

tests/msgram_mcp/
├── test_client.py
├── test_server.py
└── auth/
    └── test_msgram_auth.py
└── tools/
    ├── test_organizations.py
    ├── test_releases.py
    ├── test_supported_characteristics.py
    ├── test_supported_measures.py
    ├── test_supported_metrics.py
    └── test_entity_relationship_tree.py
```

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Configuração do ambiente

Copie os arquivos de variáveis de ambiente:

```bash
cp env-vars-example/.service.env env-vars/.service.env
cp env-vars-example/.mcp.env env-vars/.mcp.env
```

Preencha o `.mcp.env` com as credenciais:

```env
SERVICE=http://service:8080/api/v1/
MSGRAM_USER=admin
MSGRAM_PASSWORD=admin
```

---

## Subindo o projeto

```bash
docker compose -f compose.dev.yaml up --build
```

Os serviços disponíveis após subir:

| Serviço        | URL                   |
|----------------|-----------------------|
| msgram-service | http://localhost:8080 |
| mcp-server     | http://localhost:8000 |
| mcp-inspector  | http://localhost:6274 |

---

## Rodando os testes

```bash
docker compose -f compose.dev.yaml exec mcp-server pytest -v
```