
# Arquitetura do MCP

```txt
src/msgram_mcp/
├── __init__.py       # marca como pacote Python importável
├── server.py         # ponto de entrada — sobe o FastMCP e registra as tools
└── tools/
    ├── __init__.py   # marca tools/ como subpacote
    └── ola_mundo.py  # cada arquivo = um domínio de tools

tests/msgram_mcp/
├── conftest.py       # fixtures compartilhadas entre todos os testes
└── tools/
    └── test_ola_mundo.py  # espelha a estrutura de src/
```