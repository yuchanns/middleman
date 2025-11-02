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
```

## Usage

### Running the server

```bash
# Using UV
uv run python main.py

# Or activate the virtual environment
source .venv/bin/activate
python main.py
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
uv run pytest tests/
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
