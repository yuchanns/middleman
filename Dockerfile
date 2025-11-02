# Build stage for UV dependencies
FROM python:3.12-slim AS uv

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install UV
RUN pip install -U pip setuptools wheel && \
    pip install uv

# Copy project files for dependency installation
COPY pyproject.toml uv.lock ./
COPY src ./src

# Install production dependencies and the package
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev && \
    uv pip install --no-deps -e .

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Copy dependencies and application from uv stage
COPY --from=uv /app/.venv /app/.venv
COPY --from=uv /app/src /app/src

# Set environment variables
ENV PYTHONPATH="/app/.venv/lib/python3.12/site-packages:/app/src" \
    VIRTUAL_ENV="/app/.venv" \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN adduser --disabled-password --gecos "" --no-create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "-m", "middleman.main"]
