from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import asyncio
import json
import base64
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn

from emotion_detector import EmotionDetector
from vector_face_tracker import VectorFaceTracker

app = FastAPI(title="Student Concentration Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
emotion_detector = EmotionDetector()
face_tracker = VectorFaceTracker()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                self.active_connections.remove(connection)

manager = ConnectionManager()

# Camera state
camera_active = False
cap = None

@app.get("/")
async def root():
    return {"message": "Student Concentration Tracker API", "status": "running"}

@app.get("/faces")
async def get_all_faces():
    """Get all tracked faces with their statistics"""
    try:
        faces = face_tracker.get_all_faces()
        return {"faces": faces, "count": len(faces)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/faces/{face_id}")
async def get_face_by_id(face_id: str):
    """Get specific face by ID"""
    try:
        face = face_tracker.get_face_by_id(face_id)
        if face is None:
            raise HTTPException(status_code=404, detail="Face not found")
        return face
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/statistics")
async def get_statistics():
    """Get overall statistics about all tracked faces"""
    try:
        stats = face_tracker.get_face_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/camera/start")
async def start_camera():
    """Start the camera and begin detection"""
    global camera_active, cap
    
    try:
        if camera_active:
            return {"message": "Camera is already active"}
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Could not open camera")
        
        camera_active = True
        
        # Start background task for processing frames
        asyncio.create_task(process_camera_frames())
        
        return {"message": "Camera started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/camera/stop")
async def stop_camera():
    """Stop the camera"""
    global camera_active, cap
    
    try:
        camera_active = False
        if cap is not None:
            cap.release()
            cap = None
        
        return {"message": "Camera stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/camera/status")
async def get_camera_status():
    """Get camera status"""
    return {"active": camera_active}

async def process_camera_frames():
    """Background task to process camera frames"""
    global camera_active, cap
    
    frame_count = 0
    while camera_active and cap is not None:
        try:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 5th frame to reduce computational load
            frame_count += 1
            if frame_count % 5 != 0:
                await asyncio.sleep(0.033)  # ~30 FPS
                continue
            
            # Detect emotions in the frame
            detections = emotion_detector.detect_emotions_in_frame(frame)
            
            # Process each detection
            detection_results = []
            for detection in detections:
                face_encoding = detection['face_encoding']
                emotion = detection['emotion']
                confidence = detection['confidence']
                concentration = detection['concentration']
                face_image = detection['face_image']
                
                # Add or update face in vector tracker
                face_id = face_tracker.add_or_update_face(
                    face_encoding, emotion, confidence, concentration
                )
                
                detection_results.append({
                    'face_id': face_id,
                    'emotion': emotion,
                    'confidence': confidence,
                    'concentration': concentration,
                    'face_location': detection['face_location'],
                    'face_image': face_image,
                    'timestamp': detection['timestamp']
                })
            
            # Annotate frame and convert to base64
            annotated_frame = emotion_detector.annotate_frame(frame, detections)
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_b64 = base64.b64encode(buffer).decode('utf-8')
            
            # Broadcast results to all connected clients
            message = {
                'type': 'detection_update',
                'data': {
                    'detections': detection_results,
                    'frame': frame_b64,
                    'statistics': face_tracker.get_face_statistics(),
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            await manager.broadcast(json.dumps(message))
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            await asyncio.sleep(0.1)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any incoming messages
            data = await websocket.receive_text()
            # Echo back for now, can be extended for client commands
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/export/json")
async def export_data_json():
    """Export all tracking data to JSON"""
    try:
        filename = f"face_tracking_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        face_tracker.save_to_json(filename)
        return {"message": f"Data exported to {filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    global camera_active, cap
    camera_active = False
    if cap is not None:
        cap.release()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
