from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Event, RSVP, Waitlist
from ..auth import current_user

router=APIRouter(tags=["analytics"])

@router.get("/events/{event_id}/analytics")
def analytics(event_id:str,user=Depends(current_user),db:Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if e.organizer_id!=user.id and user.role!="ADMIN": raise HTTPException(403,"Forbidden")
    rows=db.query(RSVP.status,func.count(RSVP.id)).filter(RSVP.event_id==event_id).group_by(RSVP.status).all()
    c={"GOING":0,"MAYBE":0,"NOT_GOING":0}
    for s,n in rows:c[s]=n
    total=sum(c.values())
    return {
        "event_id":event_id,"total_responses":total,"going":c["GOING"],
        "maybe":c["MAYBE"],"not_going":c["NOT_GOING"],
        "response_rate":round(total/max(1,total)*100,2),
        "capacity_utilization":round(c["GOING"]/e.maximum_capacity*100,2),
        "available_seats":max(0,e.maximum_capacity-c["GOING"]),
        "waitlist_count":db.query(Waitlist).filter(Waitlist.event_id==event_id,Waitlist.status=="WAITLISTED").count()
    }
