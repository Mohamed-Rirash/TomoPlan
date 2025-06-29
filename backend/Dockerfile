FROM python:3.13-slim
WORKDIR /app

# Copy the .env file from the root directory
COPY .env .

# Copy only the backend directory contents
COPY backend/ .
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync --frozen --no-cache
CMD ["/app/.venv/bin/fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]
