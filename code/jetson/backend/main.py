import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import api_routes
import uvicorn
import json
import os

app = FastAPI(title="Potato Sorter API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routes.router)

# Frontend will be mounted at the end

main_loop = None

@app.on_event("startup")
async def startup_event():
    global main_loop
    main_loop = asyncio.get_running_loop()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws/video")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect client messages here, just keep conn open
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# A global function to be called from the vision thread to send frames
async def broadcast_frame(base64_frame: str, stats: dict, active_model: str = "Unknown", fps: float = 0.0, inf_time: float = 0.0):
    data = {
        "frame": base64_frame,
        "stats": stats,
        "active_model": active_model,
        "fps": fps,
        "inf_time": inf_time
    }
    await manager.broadcast(json.dumps(data))

# Serve the React frontend statically (MUST BE LAST ROUTE)
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
