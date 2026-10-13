from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import actions as svc

class IngestIn(BaseModel):
    title: str = Field(min_length=2)
    notes: str = Field(min_length=5)

class StatusIn(BaseModel):
    status: str

router = APIRouter()

@router.get("/board")
async def board(db: AsyncSession = Depends(get_db)):
    items = await svc.board(db)
    return {"items": [{"id": i.id, "meeting_id": i.meeting_id, "text": i.text, "owner": i.owner, "due": i.due, "status": i.status} for i in items]}

@router.post("/ingest")
async def ingest(payload: IngestIn, db: AsyncSession = Depends(get_db)):
    return await svc.ingest(db, payload.title, payload.notes)

@router.post("/{item_id}/status")
async def status(item_id: str, payload: StatusIn, db: AsyncSession = Depends(get_db)):
    try:
        item = await svc.set_status(db, item_id, payload.status)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return {"id": item.id, "status": item.status}
