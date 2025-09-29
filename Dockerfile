#misma version con la que se desarrolló
FROM python:3.13-bookworm

# Gestor de paquetes de python
COPY --from=ghcr.io/astral-sh/uv:0.8.8 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

# sincroniza las dependencias
RUN uv sync --locked

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]