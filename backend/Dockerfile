# FROM python:3.13
#
# ENV PYTHONUNBUFFERED=1
#
# WORKDIR /src/
#
# # Install uv
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
#
# # Place executables in the environment at the front of the path
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
# ENV PATH="/.venv/bin:$PATH"
#
# # Compile bytecode
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
# ENV UV_COMPILE_BYTECODE=1
#
# # uv Cache
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
# ENV UV_LINK_MODE=copy
#
# # Install dependencies
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --frozen --no-install-project
#
# ENV PYTHONPATH=/src
#
#
# COPY ./pyproject.toml ./uv.lock  /src/
#
# COPY ./src /src/src
#
# # Sync the project
# # Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
# RUN --mount=type=cache,target=/root/.cache/uv \
#     uv sync
#
# # CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
# #
#
# # Default command to run FastAPI
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
#

FROM python:3.13


ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/src

# 👇 This is the correct path where uv creates the venv inside WORKDIR (/src)
ENV VIRTUAL_ENV=/src/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /src

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Copy lock files before installing
COPY pyproject.toml uv.lock ./

# Install dependencies inside virtual env
RUN uv venv && uv pip install --upgrade pip && uv sync --frozen

# Copy the rest of the app
COPY src ./src

# Expose the app port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

