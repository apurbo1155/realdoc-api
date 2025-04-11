from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from api.auth import router as auth_router
from api.websocket import ConnectionManager
import json
import logging

logger = logging.getLogger(__name__)

app = FastAPI()
manager = ConnectionManager()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with proper prefix handling
app.include_router(api_router, prefix="/api", tags=["api"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

@app.websocket("/ws/{document_id}")
async def websocket_endpoint(websocket: WebSocket, document_id: str):
    await manager.connect(websocket, document_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get('type') == 'content_update':
                await manager.broadcast(data, document_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, document_id)

@app.get("/")
def read_root():
    return {"message": "Welcome to RealDoc API", "endpoints": {
        "websocket": "/ws/{document_id}",
        "docs": "/docs",
        "redoc": "/redoc"
    }}
