import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from middleman.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx response"""
    mock_response = AsyncMock()
    mock_response.content = b"test response content"
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    return mock_response


@pytest.mark.asyncio
async def test_proxy_dler_forwards_request(client, mock_httpx_response):
    """Test that requests are properly forwarded to dler.pro"""
    with patch("httpx.AsyncClient") as mock_client_class:
        # Setup mock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.request.return_value = mock_httpx_response

        # Make request
        response = client.get("/api/vendor/dler/api/v3/status")

        # Verify the request was forwarded correctly
        mock_client.request.assert_called_once()
        call_kwargs = mock_client.request.call_args.kwargs

        # Check target URL
        assert call_kwargs["url"] == "https://dler.pro/api/v3/status"
        assert call_kwargs["method"] == "GET"
        assert call_kwargs["follow_redirects"] is True

        # Check response
        assert response.status_code == 200
        assert response.content == b"test response content"


@pytest.mark.asyncio
async def test_proxy_dler_preserves_query_params(client, mock_httpx_response):
    """Test that query parameters are preserved"""
    with patch("httpx.AsyncClient") as mock_client_class:
        # Setup mock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.request.return_value = mock_httpx_response

        # Make request with query parameters
        response = client.get(
            "/api/vendor/dler/api/v3/download.getFile/xxxx?clash=smart"
        )

        # Verify the request was forwarded with query params
        mock_client.request.assert_called_once()
        call_kwargs = mock_client.request.call_args.kwargs

        # Check target URL includes query params
        assert (
            call_kwargs["url"]
            == "https://dler.pro/api/v3/download.getFile/xxxx?clash=smart"
        )

        # Check response
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_proxy_dler_supports_post(client, mock_httpx_response):
    """Test that POST requests are supported"""
    with patch("httpx.AsyncClient") as mock_client_class:
        # Setup mock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.request.return_value = mock_httpx_response

        # Make POST request with body
        test_body = {"key": "value"}
        response = client.post("/api/vendor/dler/api/v3/upload", json=test_body)

        # Verify the request was forwarded correctly
        mock_client.request.assert_called_once()
        call_kwargs = mock_client.request.call_args.kwargs

        # Check method
        assert call_kwargs["method"] == "POST"
        assert call_kwargs["url"] == "https://dler.pro/api/v3/upload"

        # Check response
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_proxy_dler_arbitrary_path(client, mock_httpx_response):
    """Test that arbitrary paths are supported"""
    with patch("httpx.AsyncClient") as mock_client_class:
        # Setup mock
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client.request.return_value = mock_httpx_response

        # Make request with arbitrary path
        response = client.get("/api/vendor/dler/some/random/path/here")

        # Verify the path is correctly forwarded
        mock_client.request.assert_called_once()
        call_kwargs = mock_client.request.call_args.kwargs

        assert call_kwargs["url"] == "https://dler.pro/some/random/path/here"
        assert response.status_code == 200
