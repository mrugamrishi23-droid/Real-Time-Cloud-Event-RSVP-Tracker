from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes.auth import router as auth_router
from .routes.events import router as events_router
from .routes.rsvp import router as rsvp_router
from .routes.notifications import router as notifications_router
from .routes.announcements import router as announcements_router
from .routes.analytics import router as analytics_router
from .realtime.manager import manager
from .routes.websocket import router as websocket_router

app = FastAPI(title="Real-Time Cloud Event RSVP Tracker", version="1.0.0")

origins = [x.strip() for x in __import__("os").getenv(
    "CORS_ORIGINS", "http://localhost:5173"
).split(",") if x.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(events_router, prefix="/api")
app.include_router(rsvp_router, prefix="/api")
app.include_router(notifications_router, prefix="/api")
app.include_router(announcements_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(websocket_router, prefix="/api")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"name": "Real-Time Cloud Event RSVP Tracker", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "realtime_connections": manager.count()}
