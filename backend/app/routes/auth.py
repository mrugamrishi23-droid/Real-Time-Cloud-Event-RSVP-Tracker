import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn
from ..auth import hash_password, verify_password, create_token

router = APIRouter(tags=["auth"])

@router.post("/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    user = User(
        id=str(uuid.uuid4()), name=data.name, email=data.email.lower(),
        password_hash=hash_password(data.password), role=data.role
    )
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_token(user), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": create_token(user), "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}

@router.post("/logout")
def logout():
    return {"message": "Logout complete. Delete the client-side token."}
