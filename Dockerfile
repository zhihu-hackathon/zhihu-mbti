FROM python:3.11.13-slim

WORKDIR /app
COPY ./ ./

RUN pip install uv

RUN uv sync --locked

EXPOSE 8080

ENTRYPOINT ["uv", "run", "--frozen", "--", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]