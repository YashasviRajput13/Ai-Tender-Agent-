from datetime import datetime

from jobs.celery_app import app

@app.task
def process_tender(tender_id: int, data: dict) -> dict:
    print(f"Processing tender {tender_id} at {datetime.utcnow().isoformat()}")
    return {
        "tender_id": tender_id,
        "status": "processed",
        "analysis": {
            "summary": f"Tender {data.get('title')} reviewed successfully.",
            "score": 0.8,
        },
    }

@app.task
def send_notification(recipient: str, subject: str, message: str):
    print(f"Sending notification to {recipient}: {subject}")
    return {"recipient": recipient, "status": "sent"}
