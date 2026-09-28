from collections import defaultdict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections = defaultdict(set)

    async def connect(self, event_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[event_id].add(websocket)

    def disconnect(self, event_id: str, websocket: WebSocket):
        self.connections[event_id].discard(websocket)

    async def broadcast(self, event_id: str, message: dict):
        dead = []
        for ws in self.connections[event_id]:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections[event_id].discard(ws)

    def count(self):
        return sum(len(v) for v in self.connections.values())

manager = ConnectionManager()
