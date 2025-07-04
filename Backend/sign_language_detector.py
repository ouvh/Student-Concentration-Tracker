import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json
import tensorflow as tf
from tensorflow import keras
import pickle
import os

class SignLanguageDetector:
    def __init__(self):
        """Initialize the sign language detector with MediaPipe and ML models"""
        
        # MediaPipe hands setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detector
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Sign language model (we'll create a simple one for demo)
        self.model = None
        self.label_encoder = None
        self.sequence_length = 30  # Number of frames to analyze
        self.current_sequence = []
        
        # Detection parameters
        self.detection_threshold = 0.3  # Lower threshold for better detection
        self.sign_labels = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'HELLO', 'PLEASE', 'THANK_YOU', 'YES', 'NO', 'SORRY', 'HELP'
        ]
        
        # Simple gesture detection based on hand positions
        self.use_simple_detection = True  # Use rule-based detection instead of ML model
        self.gesture_buffer = []
        self.gesture_buffer_size = 10
        
        # Detection history
        self.detection_history = []
        self.current_detection = None
        self.last_detection_time = None
        
        # Initialize the model
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize or create the sign language recognition model"""
        try:
            # For now, use simple rule-based detection
            if self.use_simple_detection:
                print("Using simple rule-based sign language detection")
                return
            
            # Try to load existing model
            if os.path.exists('model/sign_language_model.h5'):
                self.model = keras.models.load_model('model/sign_language_model.h5')
                print("Sign language model loaded successfully")
            else:
                # Create a simple demo model
                self._create_demo_model()
                
            # Load label encoder if exists
            if os.path.exists('model/sign_language_labels.pkl'):
                with open('model/sign_language_labels.pkl', 'rb') as f:
                    self.label_encoder = pickle.load(f)
            else:
                self._create_label_encoder()
                
        except Exception as e:
            print(f"Error initializing sign language model: {e}")
            print("Falling back to simple rule-based detection")
            self.use_simple_detection = True
    
    def _create_demo_model(self):
        """Create a simple demo model for sign language recognition"""
        try:
            # Simple LSTM model for gesture recognition
            model = keras.Sequential([
                keras.layers.LSTM(64, return_sequences=True, activation='relu', 
                                 input_shape=(self.sequence_length, 63)),  # 21 landmarks * 3 coordinates
                keras.layers.LSTM(128, return_sequences=True, activation='relu'),
                keras.layers.LSTM(64, return_sequences=False, activation='relu'),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dense(32, activation='relu'),
                keras.layers.Dense(len(self.sign_labels), activation='softmax')
            ])
            
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            self.model = model
            print("Demo sign language model created")
            
            # Save the model
            os.makedirs('model', exist_ok=True)
            model.save('model/sign_language_model.h5')
            
        except Exception as e:
            print(f"Error creating demo model: {e}")
            self.model = None
    
    def _create_label_encoder(self):
        """Create and save label encoder"""
        try:
            # Simple mapping for demo
            self.label_encoder = {i: label for i, label in enumerate(self.sign_labels)}
            
            # Save label encoder
            os.makedirs('model', exist_ok=True)
            with open('model/sign_language_labels.pkl', 'wb') as f:
                pickle.dump(self.label_encoder, f)
                
        except Exception as e:
            print(f"Error creating label encoder: {e}")
            self.label_encoder = {i: f"SIGN_{i}" for i in range(len(self.sign_labels))}
    
    def extract_landmarks(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """Extract hand landmarks from frame using MediaPipe"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                # Extract landmarks for the first detected hand
                landmarks = results.multi_hand_landmarks[0]
                
                # Convert landmarks to numpy array
                landmark_array = []
                for landmark in landmarks.landmark:
                    landmark_array.extend([landmark.x, landmark.y, landmark.z])
                
                return np.array(landmark_array)
            
            return None
            
        except Exception as e:
            print(f"Error extracting landmarks: {e}")
            return None
    
    def detect_sign_in_frame(self, frame: np.ndarray) -> Dict:
        """Detect sign language in a single frame"""
        try:
            # Extract landmarks
            landmarks = self.extract_landmarks(frame)
            
            if landmarks is not None:
                # Use simple rule-based detection for now
                if self.use_simple_detection:
                    prediction = self._simple_gesture_detection(landmarks)
                    if prediction:
                        return prediction
                else:
                    # Add to sequence for ML model
                    self.current_sequence.append(landmarks)
                    
                    # Maintain sequence length
                    if len(self.current_sequence) > self.sequence_length:
                        self.current_sequence.pop(0)
                    
                    # Only predict if we have enough frames
                    if len(self.current_sequence) == self.sequence_length:
                        prediction = self._predict_sign()
                        if prediction:
                            return prediction
            
            # Return empty detection if no sign detected
            return {
                'sign': None,
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat(),
                'landmarks_detected': landmarks is not None
            }
            
        except Exception as e:
            print(f"Error in sign detection: {e}")
            return {
                'sign': None,
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _simple_gesture_detection(self, landmarks: np.ndarray) -> Optional[Dict]:
        """Simple rule-based gesture detection using hand landmarks"""
        try:
            # Reshape landmarks back to 21 points with x,y,z coordinates
            landmarks_2d = landmarks.reshape(21, 3)
            
            # Add to gesture buffer for stability
            self.gesture_buffer.append(landmarks_2d)
            if len(self.gesture_buffer) > self.gesture_buffer_size:
                self.gesture_buffer.pop(0)
            
            # Only detect if we have enough frames
            if len(self.gesture_buffer) < 3:
                return None
            
            # Average the landmarks for stability
            avg_landmarks = np.mean(self.gesture_buffer, axis=0)
            
            # Simple gesture recognition based on finger positions
            detected_sign = self._classify_hand_gesture(avg_landmarks)
            
            if detected_sign:
                detection = {
                    'sign': detected_sign['sign'],
                    'confidence': detected_sign['confidence'],
                    'timestamp': datetime.now().isoformat(),
                    'detection_method': 'rule_based'
                }
                
                # Add to history
                self.detection_history.append(detection)
                self.current_detection = detection
                self.last_detection_time = datetime.now()
                
                return detection
            
            return None
            
        except Exception as e:
            print(f"Error in simple gesture detection: {e}")
            return None
    
    def _classify_hand_gesture(self, landmarks: np.ndarray) -> Optional[Dict]:
        """Classify hand gesture based on landmark positions"""
        try:
            # Extract key landmark points (using MediaPipe hand landmark indices)
            # Tip landmarks: thumb(4), index(8), middle(12), ring(16), pinky(20)
            # MCP landmarks: thumb(3), index(5), middle(9), ring(13), pinky(17)
            
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]
            
            thumb_mcp = landmarks[3]
            index_mcp = landmarks[5]
            middle_mcp = landmarks[9]
            ring_mcp = landmarks[13]
            pinky_mcp = landmarks[17]
            
            wrist = landmarks[0]
            
            # Calculate if fingers are extended (tip higher than MCP)
            thumb_up = thumb_tip[1] < thumb_mcp[1]
            index_up = index_tip[1] < index_mcp[1]
            middle_up = middle_tip[1] < middle_mcp[1]
            ring_up = ring_tip[1] < ring_mcp[1]
            pinky_up = pinky_tip[1] < pinky_mcp[1]
            
            # Count extended fingers
            extended_fingers = sum([thumb_up, index_up, middle_up, ring_up, pinky_up])
            
            # Simple gesture classification
            confidence = 0.7  # Base confidence for rule-based detection
            
            # Peace sign (V) - index and middle up, others down
            if index_up and middle_up and not ring_up and not pinky_up:
                return {'sign': 'V', 'confidence': confidence}
            
            # Thumbs up
            if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
                return {'sign': 'THUMBS_UP', 'confidence': confidence}
            
            # Open hand (5 fingers)
            if extended_fingers == 5:
                return {'sign': 'OPEN_HAND', 'confidence': confidence}
            
            # Closed fist (0 fingers)
            if extended_fingers == 0:
                return {'sign': 'FIST', 'confidence': confidence}
            
            # Pointing (index finger only)
            if index_up and not middle_up and not ring_up and not pinky_up:
                return {'sign': 'POINTING', 'confidence': confidence}
            
            # OK sign (approximate - thumb and index close)
            thumb_index_distance = np.linalg.norm(thumb_tip - index_tip)
            if thumb_index_distance < 0.05:  # Very close together
                return {'sign': 'OK', 'confidence': confidence}
            
            # Number signs
            if extended_fingers == 1:
                return {'sign': 'ONE', 'confidence': confidence}
            elif extended_fingers == 2:
                return {'sign': 'TWO', 'confidence': confidence}
            elif extended_fingers == 3:
                return {'sign': 'THREE', 'confidence': confidence}
            elif extended_fingers == 4:
                return {'sign': 'FOUR', 'confidence': confidence}
            
            # Default: detect as generic gesture
            return {'sign': f'GESTURE_{extended_fingers}', 'confidence': 0.5}
            
        except Exception as e:
            print(f"Error classifying gesture: {e}")
            return None

    def _predict_sign(self) -> Optional[Dict]:
        """Predict sign from current sequence"""
        try:
            if self.model is None or len(self.current_sequence) < self.sequence_length:
                return None
            
            # Prepare input for model
            sequence_array = np.array(self.current_sequence).reshape(1, self.sequence_length, -1)
            
            # Get prediction
            predictions = self.model.predict(sequence_array, verbose=0)
            confidence = np.max(predictions[0])
            predicted_class = np.argmax(predictions[0])
            
            # Only return prediction if confidence is high enough
            if confidence > self.detection_threshold:
                sign_label = self.label_encoder.get(predicted_class, f"UNKNOWN_{predicted_class}")
                
                detection = {
                    'sign': sign_label,
                    'confidence': float(confidence),
                    'timestamp': datetime.now().isoformat(),
                    'predicted_class': int(predicted_class)
                }
                
                # Add to history
                self.detection_history.append(detection)
                self.current_detection = detection
                self.last_detection_time = datetime.now()
                
                return detection
            
            return None
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
    
    def annotate_frame_with_landmarks(self, frame: np.ndarray) -> np.ndarray:
        """Annotate frame with hand landmarks and detection results"""
        try:
            annotated_frame = frame.copy()
            
            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
            
            # Add detection info
            if self.current_detection and self.current_detection['sign']:
                sign = self.current_detection['sign']
                confidence = self.current_detection['confidence']
                
                # Create info box
                info_text = f"Sign: {sign} ({confidence:.2f})"
                
                # Get text size
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8
                thickness = 2
                (text_width, text_height), baseline = cv2.getTextSize(info_text, font, font_scale, thickness)
                
                # Draw background rectangle
                cv2.rectangle(annotated_frame, (10, 10), (text_width + 20, text_height + 30), (0, 0, 0), -1)
                cv2.rectangle(annotated_frame, (10, 10), (text_width + 20, text_height + 30), (0, 255, 0), 2)
                
                # Draw text
                cv2.putText(annotated_frame, info_text, (15, text_height + 20), font, font_scale, (255, 255, 255), thickness)
            
            # Add status info
            status_text = f"Hands: {'Detected' if results.multi_hand_landmarks else 'Not Detected'}"
            cv2.putText(annotated_frame, status_text, (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            return annotated_frame
            
        except Exception as e:
            print(f"Error annotating frame: {e}")
            return frame
    
    def get_detection_statistics(self) -> Dict:
        """Get statistics about sign language detections"""
        if not self.detection_history:
            return {
                'total_detections': 0,
                'unique_signs': 0,
                'avg_confidence': 0.0,
                'most_common_sign': None,
                'detection_rate': 0.0
            }
        
        total_detections = len(self.detection_history)
        signs = [detection['sign'] for detection in self.detection_history if detection['sign']]
        unique_signs = len(set(signs))
        avg_confidence = np.mean([detection['confidence'] for detection in self.detection_history])
        
        # Most common sign
        most_common_sign = None
        if signs:
            sign_counts = {}
            for sign in signs:
                sign_counts[sign] = sign_counts.get(sign, 0) + 1
            most_common_sign = max(sign_counts, key=sign_counts.get)
        
        return {
            'total_detections': total_detections,
            'unique_signs': unique_signs,
            'avg_confidence': float(avg_confidence),
            'most_common_sign': most_common_sign,
            'recent_detections': self.detection_history[-10:] if self.detection_history else []
        }
    
    def get_recent_detections(self, limit: int = 20) -> List[Dict]:
        """Get recent sign language detections"""
        return self.detection_history[-limit:] if self.detection_history else []
    
    def clear_history(self):
        """Clear detection history"""
        self.detection_history = []
        self.current_detection = None
        self.current_sequence = []
        self.gesture_buffer = []
    
    def get_model_info(self) -> Dict:
        """Get information about the sign language model"""
        if self.use_simple_detection:
            return {
                'model_type': 'Rule-based + MediaPipe Hands',
                'input_features': 'Hand landmarks (21 points x 3 coordinates)',
                'detection_method': 'Geometric finger position analysis',
                'supported_gestures': ['THUMBS_UP', 'V', 'OPEN_HAND', 'FIST', 'POINTING', 'OK', 'ONE', 'TWO', 'THREE', 'FOUR'],
                'detection_threshold': self.detection_threshold,
                'model_status': 'rule_based_active'
            }
        else:
            return {
                'model_type': 'LSTM + MediaPipe Hands',
                'input_features': 'Hand landmarks (21 points x 3 coordinates)',
                'sequence_length': self.sequence_length,
                'supported_signs': len(self.sign_labels),
                'detection_threshold': self.detection_threshold,
                'model_status': 'loaded' if self.model else 'not_loaded'
            }
    
    def set_detection_threshold(self, threshold: float):
        """Set the confidence threshold for sign detection"""
        self.detection_threshold = max(0.1, min(0.99, threshold))
    
    def set_detection_mode(self, use_simple: bool = True):
        """Set the detection mode (simple rule-based or ML model)"""
        self.use_simple_detection = use_simple
        if use_simple:
            print("Switched to simple rule-based detection")
        else:
            print("Switched to ML model detection")
            if self.model is None:
                print("Warning: ML model not loaded, falling back to simple detection")
                self.use_simple_detection = True
    
    def save_detections_to_file(self, filename: str = "sign_language_detections.json") -> bool:
        """Save detection history to file"""
        try:
            data = {
                'detections': self.detection_history,
                'statistics': self.get_detection_statistics(),
                'model_info': self.get_model_info(),
                'saved_at': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving detections: {e}")
            return False

    def create_training_data_from_video(self, video_path: str, sign_label: str, output_file: str):
        """Create training data from video for a specific sign (utility function)"""
        cap = cv2.VideoCapture(video_path)
        sequences = []
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                landmarks = self.extract_landmarks(frame)
                if landmarks is not None:
                    sequences.append(landmarks)
            
            # Create sequences of the right length
            training_sequences = []
            for i in range(len(sequences) - self.sequence_length + 1):
                training_sequences.append(sequences[i:i + self.sequence_length])
            
            # Save training data
            training_data = {
                'sequences': training_sequences,
                'label': sign_label,
                'total_sequences': len(training_sequences)
            }
            
            with open(output_file, 'w') as f:
                json.dump(training_data, f, indent=2, default=str)
            
            print(f"Created {len(training_sequences)} training sequences for sign '{sign_label}'")
            
        except Exception as e:
            print(f"Error creating training data: {e}")
        finally:
            cap.release()
