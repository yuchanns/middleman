import asyncio
from fastapi import FastAPI, Request, Response
import tls_client
import os

app = FastAPI()

session = tls_client.Session(
    client_identifier="chrome_120",
    random_tls_extension_order=True
)

@app.api_route(
    "/api/vendor/dler/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
)
async def proxy_dler(path: str, request: Request):
    """
    Proxy requests to dler.pro using tls_client to bypass Cloudflare.
    """
    target_url = f"https://dler.pro/{path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    body = await request.body()

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in ["host", "content-length", "connection", "accept-encoding"]
    }
    
    headers["User-Agent"] = "FlClash/v0.8.91 clash-verge Platform/android"

    proxy = os.getenv("HTTPS_PROXY")

    def _send_request():
        try:
            return session.execute_request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
                proxy=proxy,
                timeout_seconds=30
            )
        except Exception as e:
            return str(e)

    response = await asyncio.to_thread(_send_request)

    if isinstance(response, str):
        return Response(content=f"Proxy Error: {response}", status_code=502)

    response_headers = {}
    
    excluded_headers = ["content-encoding", "transfer-encoding", "content-length", "connection"]

    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        
        if isinstance(value, list):
            response_headers[key] = ", ".join(value)
        else:
            response_headers[key] = str(value)

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=response_headers,
    )

def main():
    """Run the FastAPI server using uvicorn."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
