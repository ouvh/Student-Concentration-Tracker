import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional
import json
import os
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")

class DeviceDetector:
    def __init__(self):
        # YOLO model for state-of-the-art object detection
        self.yolo_model = None
        self.yolo_available = YOLO_AVAILABLE
        
        # Device classes mapping from COCO dataset to our categories
        self.device_classes_mapping = {
            # COCO class names to our device categories
            'cell phone': 'smartphone',
            'laptop': 'laptop',
            'tablet': 'tablet', 
            'tv': 'monitor',
            'monitor': 'monitor',
            'book': 'book',
            'mouse': 'mouse',
            'keyboard': 'keyboard',
            'remote': 'remote',
            'scissors': 'scissors',
            'teddy bear': 'toy',
            'hair drier': 'hair_drier',
            'toothbrush': 'toothbrush'
        }
        
        # Device classes we're interested in detecting
        self.target_device_classes = {
            'smartphone': 'smartphone',
            'laptop': 'laptop', 
            'tablet': 'tablet',
            'monitor': 'monitor',
            'book': 'book',
            'mouse': 'mouse',
            'keyboard': 'keyboard',
            'remote': 'remote'
        }
        
        # Device tracking history
        self.device_history = []
        self.current_devices = {}
        
        # Detection parameters
        self.detection_confidence = 0.3
        self.device_tracking_enabled = True  # Enable/disable device tracking
        
        # Initialize YOLO model
        self._initialize_yolo_model()
    
    def _initialize_yolo_model(self):
        """Initialize YOLO model for object detection"""
        if not self.yolo_available:
            print("YOLO not available, falling back to simple detection")
            return
        
        try:
            # Load YOLOv8 model (will download automatically if not present)
            # Using YOLOv8n (nano) for faster inference, can use YOLOv8s/m/l/x for better accuracy
            self.yolo_model = YOLO('yolov5s.pt')
            print("YOLO model loaded successfully")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            self.yolo_available = False
            self.yolo_model = None
    
    def detect_devices_yolo(self, frame: np.ndarray) -> List[Dict]:
        """Advanced device detection using YOLO model"""
        if not self.yolo_available or self.yolo_model is None:
            return self.detect_devices_simple(frame)
        
        devices = []
        
        try:
            # Run YOLO inference with configurable confidence
            results = self.yolo_model(frame, conf=self.detection_confidence, iou=0.5, verbose=False)
            
            # Process results
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get class name
                        class_id = int(box.cls)
                        class_name = self.yolo_model.names[class_id]
                        
                        # Check if this class is a device we're interested in
                        if class_name in self.device_classes_mapping:
                            device_type = self.device_classes_mapping[class_name]
                            confidence = float(box.conf.item())  # Convert to Python float
                            
                            # Get bounding box coordinates and convert to Python types
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(float)
                            
                            # Calculate area and aspect ratio
                            area = float((x2 - x1) * (y2 - y1))
                            aspect_ratio = float((x2 - x1) / (y2 - y1)) if (y2 - y1) > 0 else 1.0
                            
                            devices.append({
                                'type': device_type,
                                'confidence': confidence,
                                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                'area': area,
                                'aspect_ratio': aspect_ratio,
                                'original_class': class_name
                            })
        
        except Exception as e:
            print(f"Error in YOLO detection: {e}")
            return self.detect_devices_simple(frame)
        
        return devices
    
    def _ensure_json_serializable(self, obj):
        """Ensure all values in a dictionary/list are JSON serializable"""
        if isinstance(obj, dict):
            return {key: self._ensure_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._ensure_json_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.int8, np.int16, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif hasattr(obj, 'item'):  # For scalar numpy arrays
            return obj.item()
        else:
            # Final fallback for any remaining numpy types
            try:
                # Try to convert to Python native type
                if hasattr(obj, 'dtype'):
                    if 'int' in str(obj.dtype):
                        return int(obj)
                    elif 'float' in str(obj.dtype):
                        return float(obj)
                    elif 'bool' in str(obj.dtype):
                        return bool(obj)
                return obj
            except (ValueError, TypeError):
                # If all else fails, convert to string
                return str(obj)
    
    def detect_devices_simple(self, frame: np.ndarray) -> List[Dict]:
        """Simple device detection using contours and shapes"""
        devices = []
        
        # Convert to different color spaces for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Morphological operations to clean up
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area (devices should have reasonable size)
            if area < 2000 or area > 100000:
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Calculate contour properties
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # Classify based on shape and aspect ratio
            device_type = self._classify_device(aspect_ratio, area, len(approx))
            
            if device_type:
                confidence = self._calculate_confidence(aspect_ratio, area, len(approx))
                devices.append({
                    'type': device_type,
                    'confidence': float(confidence),  # Ensure Python float
                    'bbox': [int(x), int(y), int(x + w), int(y + h)],  # Ensure Python int
                    'area': float(area),  # Ensure Python float
                    'aspect_ratio': float(aspect_ratio)  # Ensure Python float
                })
        
        return devices
    
    def _classify_device(self, aspect_ratio: float, area: float, corners: int) -> Optional[str]:
        """Classify device based on geometric properties"""
        # Smartphone: tall and narrow
        if 0.3 < aspect_ratio < 0.7 and 2000 < area < 20000:
            return 'smartphone'
        
        # Laptop: wide rectangle, medium size
        elif 1.2 < aspect_ratio < 2.2 and 15000 < area < 80000:
            return 'laptop'
        
        # Tablet: square-ish, medium size
        elif 0.7 < aspect_ratio < 1.4 and 10000 < area < 50000:
            return 'tablet'
        
        # Monitor: very wide rectangle, large size
        elif aspect_ratio > 1.5 and area > 30000:
            return 'monitor'
        
        # Book/Notebook: rectangular, various sizes
        elif 0.6 < aspect_ratio < 0.9 and 5000 < area < 40000 and corners >= 4:
            return 'book'
        
        return None
    
    def _calculate_confidence(self, aspect_ratio: float, area: float, corners: int) -> float:
        """Calculate confidence score based on how well shape matches expected device"""
        base_confidence = 0.4
        
        # Adjust confidence based on how typical the measurements are
        if 4 <= corners <= 6:  # Rectangular shapes
            base_confidence += 0.2
        
        if 5000 < area < 50000:  # Reasonable device size
            base_confidence += 0.2
        
        if 0.3 < aspect_ratio < 2.5:  # Reasonable aspect ratio
            base_confidence += 0.2
        
        return min(base_confidence, 0.95)
    
    def detect_devices_in_frame(self, frame: np.ndarray) -> Dict:
        """Detect electronic devices in frame using YOLO or fallback to simple detection"""
        # Return empty result if device tracking is disabled
        if not self.device_tracking_enabled:
            return {
                'detected_devices': [],
                'device_counts': {},
                'total_devices': 0,
                'timestamp': datetime.now().isoformat(),
                'distraction_level': 'low',
                'detection_method': 'disabled',
                'tracking_enabled': False
            }
        
        # Use YOLO detection if available, otherwise fall back to simple detection
        if self.yolo_available and self.yolo_model is not None:
            detected_devices = self.detect_devices_yolo(frame)
        else:
            detected_devices = self.detect_devices_simple(frame)
        
        # Count devices by type
        device_counts = {}
        for device in detected_devices:
            device_type = device['type']
            device_counts[device_type] = device_counts.get(device_type, 0) + 1
        
        # Update current devices
        self.current_devices = device_counts
        
        # Record in history
        timestamp = datetime.now()
        history_entry = {
            'timestamp': timestamp.isoformat(),
            'devices': device_counts,
            'total_devices': sum(device_counts.values()),
            'detection_method': 'yolo' if (self.yolo_available and self.yolo_model is not None) else 'simple'
        }
        
        self.device_history.append(history_entry)
        
        # Keep only last 500 entries for performance
        if len(self.device_history) > 500:
            self.device_history = self.device_history[-500:]
        
        detection_result = {
            'detected_devices': detected_devices,
            'device_counts': device_counts,
            'total_devices': sum(device_counts.values()),
            'timestamp': timestamp.isoformat(),
            'distraction_level': self._calculate_distraction_level(device_counts),
            'detection_method': 'yolo' if (self.yolo_available and self.yolo_model is not None) else 'simple',
            'tracking_enabled': True
        }
        
        # Ensure all values are JSON serializable
        return self._ensure_json_serializable(detection_result)
    
    def _calculate_distraction_level(self, device_counts: Dict) -> str:
        """Calculate distraction level based on detected devices"""
        # Enhanced distraction weights for more device types
        distraction_weights = {
            'smartphone': 4,      # High distraction
            'tablet': 3,          # High distraction
            'laptop': 1,          # Medium distraction (could be for work)
            'monitor': 0.5,       # Low distraction (work-related)
            'book': -1,           # Negative distraction (good for learning)
            'mouse': 0.2,         # Low distraction
            'keyboard': 0.2,      # Low distraction
            'remote': 2,          # Medium distraction
            'scissors': 0.1,      # Very low distraction
            'toy': 2,             # Medium distraction
            'hair_drier': 1,      # Low distraction
            'toothbrush': 0.1     # Very low distraction
        }
        
        distraction_score = 0
        for device_type, count in device_counts.items():
            weight = distraction_weights.get(device_type, 1)
            distraction_score += count * weight
        
        # Enhanced classification with more nuanced levels
        if distraction_score <= 0:
            return 'low'
        elif distraction_score <= 1:
            return 'low'
        elif distraction_score <= 3:
            return 'medium'
        else:
            return 'high'
    
    def annotate_frame_with_devices(self, frame: np.ndarray, detection_result: Dict) -> np.ndarray:
        """Annotate frame with device detection results"""
        annotated_frame = frame.copy()
        
        # Enhanced color mapping for different device types
        device_colors = {
            'smartphone': (0, 0, 255),      # Red - High distraction
            'tablet': (0, 100, 255),        # Orange-Red - High distraction
            'laptop': (255, 100, 0),        # Blue - Work device
            'monitor': (255, 255, 0),       # Cyan - Work device
            'book': (0, 255, 0),            # Green - Educational
            'mouse': (255, 0, 255),         # Magenta - Peripheral
            'keyboard': (255, 0, 200),      # Pink - Peripheral
            'remote': (0, 255, 255),        # Yellow - Entertainment
            'scissors': (128, 128, 128),    # Gray - Tool
            'toy': (0, 150, 255),           # Orange - Distraction
            'hair_drier': (100, 100, 100),  # Dark gray - Personal item
            'toothbrush': (50, 50, 50)      # Very dark gray - Personal item
        }
        
        # Draw bounding boxes and labels
        for device in detection_result['detected_devices']:
            x1, y1, x2, y2 = device['bbox']
            device_type = device['type']
            confidence = device['confidence']
            
            color = device_colors.get(device_type, (255, 255, 255))
            
            # Draw bounding box with thickness based on confidence
            thickness = max(1, int(confidence * 3))
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, thickness)
            
            # Prepare label with confidence and type
            label = f"{device_type}: {confidence:.2f}"
            if 'original_class' in device:
                label += f" ({device['original_class']})"
            
            # Calculate label dimensions
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_thickness = 2
            (label_w, label_h), baseline = cv2.getTextSize(label, font, font_scale, font_thickness)
            
            # Draw label background
            label_y = y1 - 10 if y1 - 10 > label_h else y1 + label_h + 10
            cv2.rectangle(annotated_frame, 
                         (x1, label_y - label_h - 5), 
                         (x1 + label_w, label_y + baseline), 
                         color, -1)
            
            # Draw label text
            cv2.putText(annotated_frame, label, (x1, label_y - 5),
                       font, font_scale, (255, 255, 255), font_thickness)
        
        # Add enhanced distraction level indicator
        distraction_level = detection_result['distraction_level']
        total_devices = detection_result['total_devices']
        detection_method = detection_result.get('detection_method', 'simple')
        
        # Choose color based on distraction level
        distraction_colors = {
            'low': (0, 255, 0),      # Green
            'medium': (0, 255, 255), # Yellow
            'high': (0, 0, 255)      # Red
        }
        distraction_color = distraction_colors.get(distraction_level, (255, 255, 255))
        
        # Create status text
        status_text = f"Distraction: {distraction_level.upper()} | Devices: {total_devices} | Method: {detection_method.upper()}"
        
        # Add semi-transparent background for status
        overlay = annotated_frame.copy()
        cv2.rectangle(overlay, (5, 5), (len(status_text) * 12, 40), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, annotated_frame, 0.3, 0, annotated_frame)
        
        # Draw status text
        cv2.putText(annotated_frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, distraction_color, 2)
        
        return annotated_frame
    
    def get_current_device_summary(self) -> Dict:
        """Get current device detection summary"""
        return {
            'devices': self.current_devices,
            'total_devices': sum(self.current_devices.values()),
            'distraction_level': self._calculate_distraction_level(self.current_devices),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_device_history(self, minutes: int = 60) -> List[Dict]:
        """Get device detection history for the last N minutes"""
        if not self.device_history:
            return []
        
        now = datetime.now()
        filtered_history = []
        
        for entry in self.device_history:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            time_diff = (now - entry_time).total_seconds() / 60  # Convert to minutes
            
            if time_diff <= minutes:
                filtered_history.append(entry)
        
        return filtered_history
    
    def get_device_statistics(self) -> Dict:
        """Get overall device statistics"""
        if not self.device_history:
            return {
                'total_detections': 0,
                'device_type_counts': {},
                'avg_devices_per_detection': 0,
                'peak_device_count': 0,
                'avg_distraction_level': 'low'
            }
        
        total_detections = len(self.device_history)
        device_type_counts = {}
        total_devices = 0
        peak_count = 0
        distraction_scores = []
        
        for entry in self.device_history:
            total_devices += entry['total_devices']
            peak_count = max(peak_count, entry['total_devices'])
            
            for device_type, count in entry['devices'].items():
                device_type_counts[device_type] = device_type_counts.get(device_type, 0) + count
            
            # Calculate distraction for this entry
            distraction_level = self._calculate_distraction_level(entry['devices'])
            distraction_map = {'low': 1, 'medium': 2, 'high': 3}
            distraction_scores.append(distraction_map[distraction_level])
        
        avg_distraction_score = sum(distraction_scores) / len(distraction_scores) if distraction_scores else 1
        avg_distraction_level = 'low' if avg_distraction_score < 1.5 else 'medium' if avg_distraction_score < 2.5 else 'high'
        
        return {
            'total_detections': total_detections,
            'device_type_counts': device_type_counts,
            'avg_devices_per_detection': total_devices / total_detections if total_detections > 0 else 0,
            'peak_device_count': peak_count,
            'avg_distraction_level': avg_distraction_level
        }
    
    def clear_history(self):
        """Clear device detection history"""
        self.device_history = []
        self.current_devices = {}
    
    def get_model_info(self) -> Dict:
        """Get information about the detection model being used"""
        if self.yolo_available and self.yolo_model is not None:
            return {
                'model_type': 'YOLOv8',
                'model_file': 'yolov8n.pt',
                'available_classes': len(self.yolo_model.names),
                'target_device_classes': list(self.target_device_classes.keys()),
                'status': 'active'
            }
        else:
            return {
                'model_type': 'Simple Contour Detection',
                'model_file': 'built-in',
                'available_classes': len(self.target_device_classes),
                'target_device_classes': list(self.target_device_classes.keys()),
                'status': 'fallback'
            }
    
    def set_detection_confidence(self, confidence: float):
        """Set the confidence threshold for YOLO detection"""
        self.detection_confidence = max(0.1, min(0.9, confidence))
    
    def set_device_tracking_enabled(self, enabled: bool):
        """Enable or disable device tracking"""
        self.device_tracking_enabled = enabled
        print(f"Device tracking {'enabled' if enabled else 'disabled'}")
    
    def is_device_tracking_enabled(self) -> bool:
        """Check if device tracking is enabled"""
        return self.device_tracking_enabled
    
    def get_device_type_history(self, device_type: str, hours: int = 24) -> List[Dict]:
        """Get history for a specific device type over the last N hours"""
        if not self.device_history:
            return []
        
        now = datetime.now()
        filtered_history = []
        
        for entry in self.device_history:
            entry_time = datetime.fromisoformat(entry['timestamp'])
            time_diff = (now - entry_time).total_seconds() / 3600  # Convert to hours
            
            if time_diff <= hours:
                # Only include entries where this device type was detected
                if device_type in entry['devices'] and entry['devices'][device_type] > 0:
                    filtered_history.append({
                        'timestamp': entry['timestamp'],
                        'count': entry['devices'][device_type],
                        'total_devices': entry['total_devices'],
                        'detection_method': entry.get('detection_method', 'unknown')
                    })
        
        return filtered_history
    
    def get_device_timeline_stats(self, device_type: str, hours: int = 24) -> Dict:
        """Get comprehensive statistics for a device type over time"""
        history = self.get_device_type_history(device_type, hours)
        
        if not history:
            return {
                'device_type': device_type,
                'total_detections': 0,
                'first_seen': None,
                'last_seen': None,
                'peak_count': 0,
                'average_count': 0,
                'detection_frequency': 0,
                'timeline': []
            }
        
        # Calculate statistics
        counts = [entry['count'] for entry in history]
        timestamps = [entry['timestamp'] for entry in history]
        
        return {
            'device_type': device_type,
            'total_detections': len(history),
            'first_seen': min(timestamps),
            'last_seen': max(timestamps),
            'peak_count': max(counts),
            'average_count': sum(counts) / len(counts),
            'detection_frequency': len(history) / hours,  # detections per hour
            'timeline': history[-50:]  # Last 50 entries for timeline visualization
        }
    
    def get_all_device_types_detected(self) -> List[str]:
        """Get all device types that have been detected in history"""
        device_types = set()
        for entry in self.device_history:
            device_types.update(entry['devices'].keys())
        return sorted(list(device_types))
    
    def get_supported_devices(self) -> List[str]:
        """Get list of supported device types"""
        return list(self.target_device_classes.keys())
    
    def save_device_data(self, filename: str = "device_data.json") -> bool:
        """Save device data to file"""
        try:
            data = {
                'current_devices': self.current_devices,
                'history': self.device_history,
                'statistics': self.get_device_statistics(),
                'model_info': self.get_model_info(),
                'supported_devices': self.get_supported_devices(),
                'saved_at': datetime.now().isoformat()
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving device data: {e}")
            return False
