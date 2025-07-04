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
from device_detector import DeviceDetector
from sign_language_detector import SignLanguageDetector

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
device_detector = DeviceDetector()
sign_language_detector = SignLanguageDetector()

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

@app.get("/devices")
async def get_device_counts():
    """Get current device counts"""
    try:
        stats = device_detector.get_device_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices/history")
async def get_device_history(hours: int = 24):
    """Get device detection history for the last N hours"""
    try:
        history = device_detector.get_device_history(hours)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/devices/statistics")
async def get_device_statistics():
    """Get device detection statistics"""
    try:
        stats = device_detector.get_device_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/devices/current")
async def get_current_devices():
    """Get current device detection summary"""
    return device_detector.get_current_device_summary()

@app.get("/api/devices/statistics")
async def get_device_statistics_api():
    """Get device detection statistics for API"""
    return device_detector.get_device_statistics()

@app.get("/api/devices/history")
async def get_device_history_api(minutes: int = 60):
    """Get device detection history for API"""
    return device_detector.get_device_history(minutes)

@app.post("/api/devices/clear-history")
async def clear_device_history():
    """Clear device detection history"""
    device_detector.clear_history()
    return {"message": "Device history cleared successfully"}

@app.post("/api/devices/toggle-tracking")
async def toggle_device_tracking(enabled: bool):
    """Enable or disable device tracking"""
    device_detector.set_device_tracking_enabled(enabled)
    return {
        "message": f"Device tracking {'enabled' if enabled else 'disabled'}",
        "tracking_enabled": enabled
    }

@app.get("/api/devices/tracking-status")
async def get_device_tracking_status():
    """Get device tracking status"""
    return {
        "tracking_enabled": device_detector.is_device_tracking_enabled(),
        "model_info": device_detector.get_model_info()
    }

@app.get("/api/devices/type-history/{device_type}")
async def get_device_type_history(device_type: str, hours: int = 24):
    """Get history for a specific device type"""
    try:
        history = device_detector.get_device_type_history(device_type, hours)
        stats = device_detector.get_device_timeline_stats(device_type, hours)
        return {
            "device_type": device_type,
            "history": history,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/devices/detected-types")
async def get_detected_device_types():
    """Get all device types that have been detected"""
    try:
        return {
            "detected_types": device_detector.get_all_device_types_detected(),
            "supported_types": device_detector.get_supported_devices()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/devices/export")
async def export_device_data():
    """Export device data to JSON"""
    success = device_detector.save_device_data("device_export.json")
    if success:
        return {"message": "Device data exported successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to export device data")

# Sign Language Endpoints
@app.get("/api/signlanguage/statistics")
async def get_sign_language_statistics():
    """Get sign language detection statistics"""
    try:
        return sign_language_detector.get_detection_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/signlanguage/clear-history")
async def clear_sign_language_history():
    """Clear sign language detection history"""
    try:
        sign_language_detector.clear_history()
        return {"message": "Sign language history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            
            # Process each detection for face tracking
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
            
            # Deep learning device detection
            device_result = device_detector.detect_devices_in_frame(frame)
            
            # Annotate frame with emotions
            annotated_frame = emotion_detector.annotate_frame(frame, detections)
            
            # Annotate frame with devices
            annotated_frame = device_detector.annotate_frame_with_devices(annotated_frame, device_result)
            
            # Encode frame for streaming
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Get current statistics
            stats = face_tracker.get_face_statistics()
            
            # Prepare WebSocket message
            message = {
                "type": "detection_update",
                "data": {
                    "frame": frame_base64,
                    "detections": detection_results,
                    "devices": device_result,
                    "statistics": stats
                },
                "timestamp": datetime.now().isoformat()
            }
            
            # Broadcast results to all connected clients
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

@app.websocket("/ws/signlanguage")
async def sign_language_websocket(websocket: WebSocket):
    """WebSocket endpoint for sign language detection"""
    await websocket.accept()
    
    # Sign language detection state
    sign_language_active = False
    sign_cap = None
    processing_task = None
    
    try:
        # Send initial status
        await websocket.send_text(json.dumps({
            "type": "connected",
            "message": "Sign language WebSocket connected"
        }))
        
        while True:
            try:
                # Wait for client message with timeout
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                message = json.loads(data)
                
                if message.get("action") == "start_detection":
                    if not sign_language_active:
                        sign_language_active = True
                        sign_cap = cv2.VideoCapture(0)
                        
                        if sign_cap.isOpened():
                            await websocket.send_text(json.dumps({
                                "type": "status",
                                "message": "Sign language detection started"
                            }))
                            
                            # Start detection loop
                            processing_task = asyncio.create_task(
                                process_sign_language_frames_continuous(websocket, sign_cap)
                            )
                        else:
                            await websocket.send_text(json.dumps({
                                "type": "error",
                                "message": "Could not open camera"
                            }))
                
                elif message.get("action") == "stop_detection":
                    sign_language_active = False
                    if processing_task:
                        processing_task.cancel()
                        processing_task = None
                    if sign_cap:
                        sign_cap.release()
                        sign_cap = None
                    
                    await websocket.send_text(json.dumps({
                        "type": "status",
                        "message": "Sign language detection stopped"
                    }))
                    
            except asyncio.TimeoutError:
                # No message received, continue
                continue
    
    except WebSocketDisconnect:
        if processing_task:
            processing_task.cancel()
        if sign_cap:
            sign_cap.release()
        print("Sign language WebSocket disconnected")
    except Exception as e:
        print(f"Sign language WebSocket error: {e}")
        if processing_task:
            processing_task.cancel()
        if sign_cap:
            sign_cap.release()

async def process_sign_language_frames_continuous(websocket: WebSocket, cap):
    """Continuously process sign language detection frames"""
    frame_count = 0
    
    try:
        while cap and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every 3rd frame for better performance
            if frame_count % 3 == 0:
                # Detect sign language
                detection_result = sign_language_detector.detect_sign_in_frame(frame)
                
                # Annotate frame
                annotated_frame = sign_language_detector.annotate_frame_with_landmarks(frame)
                
                # Encode frame to base64
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame update
                await websocket.send_text(json.dumps({
                    "type": "frame_update",
                    "frame": frame_base64
                }))
                
                # Send detection if sign was detected
                if detection_result.get('sign'):
                    await websocket.send_text(json.dumps({
                        "type": "sign_detection",
                        "data": detection_result
                    }))
            
            await asyncio.sleep(0.033)  # ~30 FPS
            
    except asyncio.CancelledError:
        print("Sign language processing task cancelled")
    except Exception as e:
        print(f"Error in continuous sign language processing: {e}")
    finally:
        if cap:
            cap.release()

async def process_single_sign_frame(websocket: WebSocket, cap):
    """Process a single sign language frame"""
    try:
        ret, frame = cap.read()
        if not ret:
            return
        
        # Detect sign language
        detection_result = sign_language_detector.detect_sign_in_frame(frame)
        
        # Annotate frame
        annotated_frame = sign_language_detector.annotate_frame_with_landmarks(frame)
        
        # Encode frame to base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Send frame update
        await websocket.send_text(json.dumps({
            "type": "frame_update",
            "frame": frame_base64
        }))
        
        # Send detection if sign was detected
        if detection_result.get('sign'):
            await websocket.send_text(json.dumps({
                "type": "sign_detection",
                "data": detection_result
            }))
            
    except Exception as e:
        print(f"Error processing sign frame: {e}")

async def process_sign_language_frames(websocket: WebSocket, cap, active_flag):
    """Process sign language detection frames"""
    frame_count = 0
    
    while cap and cap.isOpened() and active_flag:
        try:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every 3rd frame for better performance
            if frame_count % 3 == 0:
                # Detect sign language
                detection_result = sign_language_detector.detect_sign_in_frame(frame)
                
                # Annotate frame
                annotated_frame = sign_language_detector.annotate_frame_with_landmarks(frame)
                
                # Encode frame to base64
                _, buffer = cv2.imencode('.jpg', annotated_frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send frame update
                await websocket.send_text(json.dumps({
                    "type": "frame_update",
                    "frame": frame_base64
                }))
                
                # Send detection if sign was detected
                if detection_result.get('sign'):
                    await websocket.send_text(json.dumps({
                        "type": "sign_detection",
                        "data": detection_result
                    }))
            
            await asyncio.sleep(0.033)  # ~30 FPS
            
        except Exception as e:
            print(f"Error in sign language processing: {e}")
            break
    
    if cap:
        cap.release()

@app.post("/export/json")
async def export_data_json():
    """Export all tracking data to JSON"""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export face tracking data
        face_filename = f"face_tracking_export_{timestamp}.json"
        face_tracker.save_to_json(face_filename)
        
        # Export device tracking data
        device_filename = f"device_tracking_export_{timestamp}.json"
        device_detector.save_device_data(device_filename)
        
        return {"message": f"Data exported to {face_filename} and {device_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system/reset-all-data")
async def reset_all_data():
    """Reset all data including face database and device history"""
    try:
        # Clear device history
        device_detector.clear_history()
        
        # Reset face tracking database
        from reset_database import reset_face_tracking_database
        reset_face_tracking_database()
        
        # Reset face tracker
        face_tracker.reset()
        
        return {"message": "All data has been reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset data: {str(e)}")

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    global camera_active, cap
    camera_active = False
    if cap is not None:
        cap.release()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
