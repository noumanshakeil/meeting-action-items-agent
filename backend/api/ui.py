from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import actions as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Meeting Action Items Agent", "items": await svc.board(db)})

@router.post("/ui/ingest")
async def ui_ingest(title: str = Form(...), notes: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.ingest(db, title, notes)
    return RedirectResponse("/", status_code=303)

@router.post("/ui/items/{item_id}/{status}")
async def ui_status(item_id: str, status: str, db: AsyncSession = Depends(get_db)):
    await svc.set_status(db, item_id, status)
    return RedirectResponse("/", status_code=303)
