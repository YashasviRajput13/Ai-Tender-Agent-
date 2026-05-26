from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Notification Service")

class NotificationRequest(BaseModel):
    recipient: str
    subject: str
    message: str
    channels: List[str] = ["email"]

class NotificationResult(BaseModel):
    status: str
    delivered: bool
    channels: List[str]

sent_notifications = []

@app.post("/notifications/send", response_model=NotificationResult)
async def send_notification(payload: NotificationRequest):
    sent_notifications.append(payload.dict())
    return NotificationResult(status="queued", delivered=True, channels=payload.channels)

@app.get("/notifications/alerts")
async def list_alerts():
    return {"alerts": sent_notifications}

@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification"}
