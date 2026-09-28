from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

Role = Literal["ATTENDEE", "ORGANIZER", "ADMIN"]
RSVPStatus = Literal["GOING", "MAYBE", "NOT_GOING"]

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6)
    role: Role = "ATTENDEE"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class EventIn(BaseModel):
    event_name: str
    description: str = ""
    event_type: str = "Workshop"
    event_date: str
    start_time: str
    end_time: str
    venue: str = ""
    online_link: Optional[str] = None
    maximum_capacity: int = Field(gt=0, le=100000)
    registration_deadline: str
    status: str = "PUBLISHED"

class RSVPIn(BaseModel):
    status: RSVPStatus

class AnnouncementIn(BaseModel):
    title: str
    message: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict
