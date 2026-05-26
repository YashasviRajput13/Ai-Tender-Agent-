import os
from typing import Dict

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt

app = FastAPI(title="Agentic AI Tender API Gateway")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
    "tender": os.getenv("TENDER_SERVICE_URL", "http://tender-service:8002"),
    "analysis": os.getenv("ANALYSIS_SERVICE_URL", "http://analysis-service:8003"),
    "notification": os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8004"),
}

async def verify_jwt(authorization: str = Header(...)) -> Dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/health")
async def health():
    return {"status": "ok", "services": SERVICES}

async def proxy_request(service: str, request: Request, jwt_payload: Dict | None = None):
    url = SERVICES[service] + request.url.path
    async with httpx.AsyncClient() as client:
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
        if jwt_payload:
            headers["x-user"] = jwt_payload.get("sub", "anonymous")
        response = await client.request(
            request.method,
            url,
            headers=headers,
            params=request.query_params,
            content=await request.body(),
        )
    return response.json()

@app.post("/auth/login")
async def login(request: Request):
    return await proxy_request("auth", request)

@app.get("/tenders")
async def list_tenders(request: Request, jwt_payload: Dict = Depends(verify_jwt)):
    return await proxy_request("tender", request, jwt_payload)

@app.post("/tenders")
async def create_tender(request: Request, jwt_payload: Dict = Depends(verify_jwt)):
    return await proxy_request("tender", request, jwt_payload)

@app.get("/analysis/score")
async def score_tender(request: Request, jwt_payload: Dict = Depends(verify_jwt)):
    return await proxy_request("analysis", request, jwt_payload)

@app.post("/notifications/send")
async def send_notification(request: Request, jwt_payload: Dict = Depends(verify_jwt)):
    return await proxy_request("notification", request, jwt_payload)
