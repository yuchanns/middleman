# middleman

A FastAPI-based HTTP proxy for forwarding requests to third-party services.

## Features

- Proxy HTTP requests to third-party services
- Preserves query parameters, headers, and request bodies
- Supports all HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- Route prefix: `/api/vendor/`

## Requirements

- Python 3.12+
- UV package manager

## Installation

```bash
# Install dependencies
uv sync

# Install the package in editable mode (for development)
uv pip install -e .
```

## Usage

### Running the server

```bash
# Using the CLI command
uv run middleman

# Or directly with Python
uv run python -m middleman.main

# Or activate the virtual environment
source .venv/bin/activate
middleman
```

The server will start on `http://0.0.0.0:8000`.

### Example

When you request:
```
http://localhost:8000/api/vendor/dler/api/v3/download.getFile/xxxx?clash=smart
```

The proxy will forward the request to:
```
https://dler.pro/api/v3/download.getFile/xxxx?clash=smart
```

## Testing

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v tests/
```

## Linting and Formatting

```bash
# Check code with ruff
uv run ruff check .

# Format code with ruff
uv run ruff format .

# Fix issues automatically
uv run ruff check --fix .
```

## Routes

### `/api/vendor/dler/{path:path}`

Forwards requests to `https://dler.pro/{path}` with the same method, headers, query parameters, and body.

## Development

This project uses:
- **Package Manager**: UV (https://github.com/astral-sh/uv)
- **Framework**: FastAPI
- **HTTP Client**: httpx
- **ASGI Server**: uvicorn
- **Testing**: pytest, pytest-asyncio
- **Linting**: ruff

## Project Structure

```
middleman/
├── src/
│   └── middleman/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_proxy.py
├── pyproject.toml
├── .gitignore
└── README.md
```

