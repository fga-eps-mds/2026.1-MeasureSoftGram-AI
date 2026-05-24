FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir --prefix=/install -e "."


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app/src src/

CMD ["python", "src/msgram_mcp/server.py"]


FROM runtime AS dev

COPY . .

RUN pip install --no-cache-dir -e ".[dev]"

CMD ["watchfiles", "python src/msgram_mcp/server.py", "src/"]