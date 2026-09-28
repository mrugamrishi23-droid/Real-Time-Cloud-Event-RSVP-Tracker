from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Notification
from ..auth import current_user

router=APIRouter(tags=["notifications"])

@router.get("/notifications")
def notifications(user=Depends(current_user), db:Session=Depends(get_db)):
    return [{"id":n.id,"event_id":n.event_id,"type":n.type,"message":n.message,
             "read":n.read,"created_at":n.created_at}
            for n in db.query(Notification).filter(Notification.user_id==user.id)
            .order_by(Notification.created_at.desc()).limit(100).all()]

@router.put("/notifications/{notification_id}/read")
def mark_read(notification_id:str,user=Depends(current_user),db:Session=Depends(get_db)):
    n=db.get(Notification,notification_id)
    if not n or n.user_id!=user.id: raise HTTPException(404,"Notification not found")
    n.read=True; db.commit()
    return {"message":"Notification marked read"}
