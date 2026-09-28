import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Announcement, Event, RSVP, Notification
from ..schemas import AnnouncementIn
from ..auth import current_user
from ..realtime.manager import manager

router=APIRouter(tags=["announcements"])

@router.post("/events/{event_id}/announcements")
async def create_announcement(event_id:str,data:AnnouncementIn,user=Depends(current_user),db:Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if e.organizer_id!=user.id and user.role!="ADMIN": raise HTTPException(403,"Forbidden")
    a=Announcement(id=str(uuid.uuid4()),event_id=event_id,title=data.title,message=data.message)
    db.add(a)
    for r in db.query(RSVP).filter(RSVP.event_id==event_id,RSVP.status.in_(["GOING","MAYBE"])).all():
        db.add(Notification(id=str(uuid.uuid4()),user_id=r.user_id,event_id=event_id,
                            type="ANNOUNCEMENT",message=data.message))
    db.commit()
    await manager.broadcast(event_id,{"type":"announcement","title":a.title,"message":a.message})
    return {"id":a.id,"title":a.title,"message":a.message,"created_at":a.created_at}

@router.get("/events/{event_id}/announcements")
def list_announcements(event_id:str,db:Session=Depends(get_db)):
    return [{"id":a.id,"title":a.title,"message":a.message,"created_at":a.created_at}
            for a in db.query(Announcement).filter(Announcement.event_id==event_id)
            .order_by(Announcement.created_at.desc()).all()]
