from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(240))
    notes: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
class ActionItem(Base):
    __tablename__ = "action_items"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    meeting_id: Mapped[str] = mapped_column(String(32), index=True)
    text: Mapped[str] = mapped_column(Text)
    owner: Mapped[str] = mapped_column(String(120), default="unassigned")
    due: Mapped[str] = mapped_column(String(32), default="")
    status: Mapped[str] = mapped_column(String(32), default="todo", index=True)
