from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint, Text, Boolean
from sqlalchemy.orm import relationship
from .database import Base

def now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="ATTENDEE")
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

class Event(Base):
    __tablename__ = "events"
    id = Column(String, primary_key=True)
    organizer_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    event_name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    event_type = Column(String(80), default="Workshop")
    event_date = Column(String(10), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    venue = Column(String(255), default="")
    online_link = Column(String(500), nullable=True)
    maximum_capacity = Column(Integer, nullable=False)
    registration_deadline = Column(String(30), nullable=False)
    status = Column(String(30), default="PUBLISHED")
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)
    organizer = relationship("User")

class RSVP(Base):
    __tablename__ = "rsvps"
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String(30), nullable=False)
    responded_at = Column(DateTime(timezone=True), default=now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=now, onupdate=now, nullable=False)
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_user_rsvp"),)

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=True)
    type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now, nullable=False)

class Waitlist(Base):
    __tablename__ = "waitlist"
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), default=now, nullable=False)
    status = Column(String(30), default="WAITLISTED")
    __table_args__ = (UniqueConstraint("event_id", "user_id", name="uq_event_user_waitlist"),)
