import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.api_route(
    "/api/vendor/dler/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def proxy_dler(path: str, request: Request):
    """
    Proxy requests to dler.pro.
    Extracts the path after /api/vendor/dler/ and forwards to https://dler.pro/
    """
    # Construct the target URL
    target_url = f"https://dler.pro/{path}"

    # Preserve query parameters
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    # Forward the request using httpx
    async with httpx.AsyncClient() as client:
        # Get the request body
        body = await request.body()

        # Forward the request with the same method, headers, and body
        response = await client.request(
            method=request.method,
            url=target_url,
            headers={
                key: value
                for key, value in request.headers.items()
                if key.lower() not in ["host", "content-length"]
            },
            content=body,
            follow_redirects=True,
        )

        # Return the response with the same status code, headers, and content
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers={
                key: value
                for key, value in response.headers.items()
                if key.lower() not in ["content-encoding", "transfer-encoding"]
            },
        )


def main():
    """Run the FastAPI server using uvicorn."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
