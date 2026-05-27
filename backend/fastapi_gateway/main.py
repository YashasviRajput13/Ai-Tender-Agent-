import os
from typing import Dict, List

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response, WebSocket, WebSocketDisconnect, status
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
ALLOW_PUBLIC_TENDERS = os.getenv("ALLOW_PUBLIC_TENDERS", "true").lower() in ("1", "true", "yes")

SERVICES = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "tender": os.getenv("TENDER_SERVICE_URL", "http://localhost:8002"),
    "analysis": os.getenv("ANALYSIS_SERVICE_URL", "http://localhost:8003"),
    "notification": os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004"),
}


def verify_jwt_token(authorization: str) -> Dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def verify_jwt(authorization: str = Header(...)) -> Dict:
    return verify_jwt_token(authorization)


async def optional_jwt(authorization: str | None = Header(None)) -> Dict | None:
    if authorization is None:
        if ALLOW_PUBLIC_TENDERS:
            return None
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required")
    return verify_jwt_token(authorization)


@app.get("/health")
async def health():
    health_status = {"status": "healthy", "database": "disconnected"}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{SERVICES['tender']}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("connection") == "PASS" or data.get("select_1") is True:
                    health_status["database"] = "connected"
                else:
                    health_status["database"] = "disconnected"
            else:
                health_status["status"] = "degraded"
    except Exception:
        health_status["status"] = "degraded"
    return health_status


async def proxy_request(service: str, request: Request, jwt_payload: Dict | None = None):
    target_path = request.url.path
    if target_path.endswith("/") and target_path != "/":
        target_path = target_path.rstrip("/")
    url = SERVICES[service] + target_path
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
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
    content = response.content
    headers = {
        k: v
        for k, v in response.headers.items()
        if k.lower() not in ("content-length", "transfer-encoding", "content-encoding", "connection")
    }
    return Response(content=content, status_code=response.status_code, headers=headers, media_type=response.headers.get("content-type"))


@app.post("/auth/login")
async def login(request: Request):
    return await proxy_request("auth", request)


@app.api_route("/tenders", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_tenders_root(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/tenders/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_tender_routes(path: str, request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/scrape/start", methods=["POST"])
async def proxy_scrape_start(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/scrape/status", methods=["GET"])
async def proxy_scrape_status(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/scrape/logs", methods=["GET"])
async def proxy_scrape_logs(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/analysis/{path:path}", methods=["GET", "POST", "PUT", "PATCH"])
async def proxy_analysis_routes(path: str, request: Request, jwt_payload: Dict = Depends(verify_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/recommendations", methods=["GET"])
async def proxy_recommendations(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/dashboard/stats", methods=["GET"])
async def proxy_dashboard_stats(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


@app.api_route("/notifications", methods=["GET", "POST"])
async def proxy_notifications(request: Request, jwt_payload: Dict | None = Depends(optional_jwt)):
    return await proxy_request("tender", request, jwt_payload)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()


@app.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.post("/events")
async def event_push(payload: dict):
    await manager.broadcast(payload)
    return {"status": "broadcasted"}
