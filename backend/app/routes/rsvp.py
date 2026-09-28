import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from ..database import get_db
from ..models import Event, RSVP, Waitlist, Notification
from ..schemas import RSVPIn
from ..auth import current_user
from ..realtime.manager import manager

router = APIRouter(tags=["rsvp"])

def counts(db, event_id):
    rows=db.query(RSVP.status, func.count(RSVP.id)).filter(RSVP.event_id==event_id).group_by(RSVP.status).all()
    c={"GOING":0,"MAYBE":0,"NOT_GOING":0}
    for s,n in rows: c[s]=n
    return c

@router.post("/events/{event_id}/rsvp")
async def upsert_rsvp(event_id: str, data: RSVPIn, user=Depends(current_user), db: Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if e.status in ("CANCELLED","COMPLETED"): raise HTTPException(400,"Event is not accepting RSVPs")
    now=datetime.now(timezone.utc)
    try:
        deadline=datetime.fromisoformat(e.registration_deadline.replace("Z","+00:00"))
        if now > deadline: raise HTTPException(400,"Registration deadline has passed")
    except ValueError:
        pass

    existing=db.query(RSVP).filter(RSVP.event_id==event_id, RSVP.user_id==user.id).first()
    c=counts(db)
    if data.status=="GOING" and (not existing or existing.status!="GOING") and c["GOING"] >= e.maximum_capacity:
        # Optional FIFO waitlist entry.
        if not db.query(Waitlist).filter(Waitlist.event_id==event_id,Waitlist.user_id==user.id).first():
            db.add(Waitlist(id=str(uuid.uuid4()),event_id=event_id,user_id=user.id))
            db.commit()
        raise HTTPException(409,"Event is full. You were added to the waitlist.")
    if existing:
        existing.status=data.status
        existing.updated_at=now
    else:
        existing=RSVP(id=str(uuid.uuid4()),event_id=event_id,user_id=user.id,status=data.status)
        db.add(existing)
    if data.status=="GOING":
        db.query(Waitlist).filter(Waitlist.event_id==event_id,Waitlist.user_id==user.id).delete()
    db.add(Notification(id=str(uuid.uuid4()),user_id=user.id,event_id=event_id,
                        type="RSVP",message=f"RSVP updated to {data.status}"))
    db.commit()
    c=counts(db)
    if c["GOING"] >= e.maximum_capacity and e.status=="PUBLISHED":
        e.status="FULL"; db.commit()
    elif c["GOING"] < e.maximum_capacity and e.status=="FULL":
        e.status="PUBLISHED"; db.commit()
    payload={"type":"rsvp_update","event_id":event_id,"counts":c,
             "available_capacity":max(0,e.maximum_capacity-c["GOING"]),"status":e.status}
    await manager.broadcast(event_id,payload)
    return payload

@router.get("/events/{event_id}/rsvps")
def get_event_rsvps(event_id: str, user=Depends(current_user), db: Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if e.organizer_id!=user.id and user.role!="ADMIN": raise HTTPException(403,"Forbidden")
    return [{"id":r.id,"user_id":r.user_id,"status":r.status,"updated_at":r.updated_at} for r in db.query(RSVP).filter(RSVP.event_id==event_id).all()]

@router.get("/rsvps/me")
def my_rsvps(user=Depends(current_user), db: Session=Depends(get_db)):
    return [{"id":r.id,"event_id":r.event_id,"status":r.status,"updated_at":r.updated_at}
            for r in db.query(RSVP).filter(RSVP.user_id==user.id).all()]

@router.delete("/events/{event_id}/rsvp")
async def cancel_rsvp(event_id: str, user=Depends(current_user), db: Session=Depends(get_db)):
    r=db.query(RSVP).filter(RSVP.event_id==event_id,RSVP.user_id==user.id).first()
    if not r: raise HTTPException(404,"RSVP not found")
    r.status="NOT_GOING"
    db.commit()
    c=counts(db)
    await manager.broadcast(event_id,{"type":"rsvp_update","event_id":event_id,"counts":c})
    return {"message":"RSVP cancelled","counts":c}
