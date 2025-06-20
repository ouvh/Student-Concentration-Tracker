import cv2
import numpy as np
import face_recognition
from keras.models import load_model
from datetime import datetime
import asyncio
import base64
from typing import List, Dict, Tuple
import os

IMG_SIZE = (48, 48)

class EmotionDetector:
    def __init__(self, model_path: str = "model/best_vgg16_improved_v2_model.keras"):
        self.model_path = model_path
        self.model = None
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.load_model()
    
    def load_model(self):
        """Load the emotion detection model"""
        try:
            self.model = load_model(self.model_path)
            print("Emotion detection model loaded successfully")
        except Exception as e:
            print(f"Error loading model from {self.model_path}: {e}")
            # Try alternative paths
            alternative_paths = [
                "best_vgg16_improved_v2_model.keras",
                "model/best_vgg16_improved_model.keras",
                "best_vgg16_improved_model.keras"
            ]
            
            for alt_path in alternative_paths:
                try:
                    self.model = load_model(alt_path)
                    print(f"Model loaded successfully from {alt_path}")
                    break
                except:
                    continue
            
            if self.model is None:
                print("Could not load any emotion detection model")
                print("Please ensure the model file exists in the correct location")
    
    def calculate_concentration(self, prediction: np.ndarray) -> float:
        """Calculate concentration score based on emotion predictions"""
        concentration_weights = {
            'angry': 0.2,
            'disgust': 0.1,
            'fear': 0.3,
            'happy': 0.9,
            'neutral': 1.0,
            'sad': 0.3,
            'surprise': 0.6
        }
        
        concentration = 0.0
        for i, emotion in enumerate(self.emotion_labels):
            weight = concentration_weights.get(emotion, 0.5)
            concentration += prediction[i] * weight
        
        return min(max(concentration * 100, 0), 100)  # Clamp between 0-100
    
    def detect_emotions_in_frame(self, frame: np.ndarray) -> List[Dict]:
        """Detect faces and emotions in a frame"""
        if self.model is None:
            return []
        
        results = []
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces using face_recognition for better accuracy
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Extract face for emotion detection
            face_img = frame[top:bottom, left:right]
            
            if face_img.size == 0:
                continue
            
            # Prepare face for emotion model
            face_img_resized = cv2.resize(face_img, IMG_SIZE)
            face_img_normalized = face_img_resized.astype('float32') / 255.0
            face_img_expanded = np.expand_dims(face_img_normalized, axis=0)
            
            # Predict emotion
            try:
                prediction = self.model.predict(face_img_expanded, verbose=0)[0]
                max_index = int(np.argmax(prediction))
                emotion = self.emotion_labels[max_index]
                confidence = float(prediction[max_index] * 100)
                concentration = self.calculate_concentration(prediction)
                
                # Convert face image to base64 for transmission
                _, buffer = cv2.imencode('.jpg', face_img)
                face_image_b64 = base64.b64encode(buffer).decode('utf-8')
                
                results.append({
                    'face_encoding': face_encoding,
                    'face_location': {'top': top, 'right': right, 'bottom': bottom, 'left': left},
                    'emotion': emotion,
                    'confidence': confidence,
                    'concentration': concentration,
                    'face_image': face_image_b64,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                print(f"Error predicting emotion: {e}")
                continue
        
        return results
    
    def annotate_frame(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """Annotate frame with detection results"""
        annotated_frame = frame.copy()
        
        for detection in detections:
            loc = detection['face_location']
            emotion = detection['emotion']
            confidence = detection['confidence']
            concentration = detection['concentration']
            
            # Draw rectangle around face
            cv2.rectangle(annotated_frame, (loc['left'], loc['top']), 
                         (loc['right'], loc['bottom']), (0, 255, 0), 2)
            
            # Add text labels
            label_y = loc['top'] - 10
            cv2.putText(annotated_frame, f"{emotion}: {confidence:.1f}%", 
                       (loc['left'], label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            label_y -= 20
            cv2.putText(annotated_frame, f"Concentration: {concentration:.1f}%", 
                       (loc['left'], label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        return annotated_frame
