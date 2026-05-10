FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir -e ".[dev]"

COPY . .

CMD ["watchfiles", "python src/msgram_mcp/server.py", "src/"]