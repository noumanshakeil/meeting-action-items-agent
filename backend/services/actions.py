from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import ActionItem, Meeting

async def ingest(session: AsyncSession, title: str, notes: str) -> dict:
    meeting = Meeting(id=uuid.uuid4().hex[:10], title=title.strip(), notes=notes.strip())
    session.add(meeting)
    await session.flush()
    llm = get_llm()
    raw = await llm.complete(
        f"Extract action items. Prefer lines: OWNER | DUE | TEXT\nNOTES:\n{notes}",
        system="You are a project manager. Extract concrete action items only.",
    )
    created = 0
    for line in raw.splitlines():
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        owner, due, text = parts[0][:80], parts[1][:32], parts[2][:500]
        if len(text) < 3:
            continue
        session.add(ActionItem(id=uuid.uuid4().hex[:10], meeting_id=meeting.id, text=text, owner=owner or "unassigned", due=due))
        created += 1
    if created == 0:
        session.add(ActionItem(id=uuid.uuid4().hex[:10], meeting_id=meeting.id, text="Follow up on meeting outcomes", owner="facilitator", due=""))
    await session.commit()
    items = list((await session.execute(select(ActionItem).where(ActionItem.meeting_id == meeting.id))).scalars())
    return {
        "meeting_id": meeting.id,
        "actions": [{"id": i.id, "text": i.text, "owner": i.owner, "due": i.due, "status": i.status} for i in items],
    }

async def board(session: AsyncSession) -> list[ActionItem]:
    result = await session.execute(select(ActionItem).order_by(ActionItem.id.desc()).limit(100))
    return list(result.scalars())

async def set_status(session: AsyncSession, item_id: str, status: str) -> ActionItem:
    item = await session.get(ActionItem, item_id)
    if not item:
        raise ValueError("not found")
    if status not in {"todo", "doing", "done"}:
        raise ValueError("bad status")
    item.status = status
    await session.commit()
    await session.refresh(item)
    return item
