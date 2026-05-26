from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Tender Service")

class TenderCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    region: str
    category: str
    value: float
    requirements: List[str]

class Tender(TenderCreate):
    id: int
    created_at: datetime

fake_tenders = [
    Tender(
        id=1,
        title="Infrastructure Maintenance Contract",
        description="Maintenance and repairs for state-owned facilities.",
        deadline=datetime.utcnow(),
        region="North America",
        category="Construction",
        value=750000.0,
        requirements=["ISO 9001", "5 years experience", "local partner"],
        created_at=datetime.utcnow(),
    )
]

@app.get("/tenders", response_model=List[Tender])
async def list_tenders(region: Optional[str] = None, category: Optional[str] = None):
    results = fake_tenders
    if region:
        results = [t for t in results if t.region.lower() == region.lower()]
    if category:
        results = [t for t in results if t.category.lower() == category.lower()]
    return results

@app.post("/tenders", response_model=Tender)
async def create_tender(payload: TenderCreate):
    tender = Tender(id=len(fake_tenders) + 1, created_at=datetime.utcnow(), **payload.dict())
    fake_tenders.append(tender)
    return tender

@app.get("/tenders/{tender_id}", response_model=Tender)
async def get_tender(tender_id: int):
    for tender in fake_tenders:
        if tender.id == tender_id:
            return tender
    raise HTTPException(status_code=404, detail="Tender not found")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "tender"}
