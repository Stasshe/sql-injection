FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked

COPY server.py ./
COPY public ./public

EXPOSE 3000
CMD ["uv", "run", "server.py"]
