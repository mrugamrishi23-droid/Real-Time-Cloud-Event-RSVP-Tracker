import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Event, RSVP
from ..schemas import EventIn
from ..auth import current_user, require_role
from datetime import datetime

router = APIRouter(tags=["events"])

def serialize(e, db):
    counts = {"GOING": 0, "MAYBE": 0, "NOT_GOING": 0}
    for r in db.query(RSVP).filter(RSVP.event_id == e.id).all():
        counts[r.status] = counts.get(r.status, 0) + 1
    return {k: getattr(e, k) for k in [
        "id","organizer_id","event_name","description","event_type","event_date",
        "start_time","end_time","venue","online_link","maximum_capacity",
        "registration_deadline","status","created_at","updated_at"
    ]} | {"counts": counts, "available_capacity": max(0, e.maximum_capacity-counts["GOING"])}

@router.post("/events")
def create_event(data: EventIn, user=Depends(require_role("ORGANIZER","ADMIN")), db: Session=Depends(get_db)):
    if data.start_time >= data.end_time:
        raise HTTPException(400, "End time must be after start time")
    e = Event(id=str(uuid.uuid4()), organizer_id=user.id, **data.model_dump())
    db.add(e); db.commit(); db.refresh(e)
    return serialize(e, db)

@router.get("/events")
def get_events(db: Session=Depends(get_db)):
    return [serialize(e, db) for e in db.query(Event).order_by(Event.event_date, Event.start_time).all()]

@router.get("/events/upcoming")
def upcoming(db: Session=Depends(get_db)):
    today = datetime.now().date().isoformat()
    return [serialize(e, db) for e in db.query(Event).filter(Event.event_date >= today, Event.status != "CANCELLED").all()]

@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session=Depends(get_db)):
    e = db.get(Event, event_id)
    if not e: raise HTTPException(404, "Event not found")
    return serialize(e, db)

@router.put("/events/{event_id}")
def update_event(event_id: str, data: EventIn, user=Depends(current_user), db: Session=Depends(get_db)):
    e = db.get(Event, event_id)
    if not e: raise HTTPException(404, "Event not found")
    if e.organizer_id != user.id and user.role != "ADMIN": raise HTTPException(403, "Not your event")
    for k,v in data.model_dump().items(): setattr(e, k, v)
    db.commit(); db.refresh(e)
    return serialize(e, db)

@router.delete("/events/{event_id}")
def delete_event(event_id: str, user=Depends(current_user), db: Session=Depends(get_db)):
    e = db.get(Event, event_id)
    if not e: raise HTTPException(404, "Event not found")
    if e.organizer_id != user.id and user.role != "ADMIN": raise HTTPException(403, "Not your event")
    e.status = "CANCELLED"
    db.commit()
    return {"message": "Event cancelled"}

@router.get("/events/{event_id}/attendees")
def attendees(event_id: str, user=Depends(current_user), db: Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if e.organizer_id != user.id and user.role!="ADMIN": raise HTTPException(403,"Forbidden")
    rows=db.query(RSVP).filter(RSVP.event_id==event_id).all()
    return [{"user_id":r.user_id,"status":r.status,"updated_at":r.updated_at} for r in rows]
