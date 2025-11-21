from fastapi import Request, Response

async def log_middleware(request: Request, call_next):
    print(f"\n{'='*20} START REQUEST {'='*20}")
    print(f"METHOD: {request.method}")
    print(f"URL: {request.url}")
    
    # Read and log request body
    try:
        body = await request.body()
        if body:
            print(f"BODY: {body.decode()}")
    except Exception as e:
        print(f"Could not read body: {e}")
        body = b""

    # Restore request body for the actual handler
    async def receive():
        return {"type": "http.request", "body": body}
    request._receive = receive

    response = await call_next(request)

    print(f"{'-'*20} RESPONSE {'-'*20}")
    print(f"STATUS: {response.status_code}")

    # Read and log response body
    res_body = b""
    async for chunk in response.body_iterator:
        res_body += chunk
    
    try:
        print(f"BODY: {res_body.decode()}")
    except Exception as e:
        print(f"Could not read response body: {e}")

    print(f"{'='*20} END REQUEST {'='*20}\n")

    # Reconstruct response
    return Response(
        content=res_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
