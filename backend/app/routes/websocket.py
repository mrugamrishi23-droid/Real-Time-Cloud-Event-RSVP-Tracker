from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..realtime.manager import manager

router=APIRouter(tags=["realtime"])

@router.websocket("/ws/events/{event_id}")
async def event_socket(websocket: WebSocket, event_id: str):
    await manager.connect(event_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(event_id, websocket)
    except Exception:
        manager.disconnect(event_id, websocket)
