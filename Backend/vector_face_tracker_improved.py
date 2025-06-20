import asyncio
import base64
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import uuid
import chromadb
from chromadb.config import Settings
import json
from sklearn.metrics.pairwise import cosine_similarity

class FaceVector:
    def __init__(self, face_id: str, encoding: np.ndarray, first_seen: datetime, 
                 last_seen: datetime, emotions: List[Dict], concentration_scores: List[float]):
        self.face_id = face_id
        self.encoding = encoding
        self.first_seen = first_seen
        self.last_seen = last_seen
        self.emotions = emotions  # List of {emotion: str, confidence: float, timestamp: datetime}
        self.concentration_scores = concentration_scores
        self.total_detections = len(emotions)

    def to_dict(self):
        return {
            'face_id': self.face_id,
            'first_seen': self.first_seen.isoformat(),
            'last_seen': self.last_seen.isoformat(),
            'emotions': self.emotions,
            'concentration_scores': self.concentration_scores,
            'total_detections': self.total_detections,
            'avg_concentration': np.mean(self.concentration_scores) if self.concentration_scores else 0,
            'dominant_emotion': max(set([e['emotion'] for e in self.emotions]), 
                                  key=[e['emotion'] for e in self.emotions].count) if self.emotions else 'unknown'
        }

class VectorFaceTracker:
    def __init__(self, similarity_threshold: float = 0.45):  # Lower threshold for better matching
        self.similarity_threshold = similarity_threshold
        self.tracked_faces: Dict[str, FaceVector] = {}
        
        # Initialize ChromaDB for vector storage
        self.chroma_client = chromadb.PersistentClient(path="./face_vectors_db")
        try:
            self.collection = self.chroma_client.get_collection("face_encodings")
            print("Successfully connected to existing face_encodings collection")
        except:
            self.collection = self.chroma_client.create_collection(
                name="face_encodings",
                metadata={"hnsw:space": "cosine"}
            )
            print("Created new face_encodings collection")
    
    def _encode_face_embedding(self, encoding: np.ndarray) -> str:
        """Convert numpy array to base64 string for storage"""
        return base64.b64encode(encoding.tobytes()).decode('utf-8')
    
    def _decode_face_embedding(self, encoded_str: str) -> np.ndarray:
        """Convert base64 string back to numpy array"""
        return np.frombuffer(base64.b64decode(encoded_str), dtype=np.float64)

    def find_matching_face(self, face_encoding: np.ndarray) -> Optional[str]:
        """Find if this face encoding matches any existing tracked face using ChromaDB's vector search"""
        if not self.tracked_faces:
            return None
        
        # Use ChromaDB for vector search when we have faces
        try:
            # Query the collection with the new face encoding
            results = self.collection.query(
                query_embeddings=[face_encoding.tolist()],
                n_results=5  # Get top 5 matches to handle multiple similar faces
            )
            
            if not results or not results['ids'] or not results['ids'][0]:
                return None
                
            # Check distances (ChromaDB returns cosine distances)
            distances = results['distances'][0]
            ids = results['ids'][0]
            
            # In cosine distance, lower values mean more similar
            # Convert distance to similarity (1 - distance)
            for i, distance in enumerate(distances):
                similarity = 1.0 - distance
                
                # Debug output to help tune the threshold
                print(f"Face match candidate: {ids[i]}, similarity: {similarity}")
                
                if similarity > self.similarity_threshold:
                    # Additional verification - compare with stored encoding
                    if ids[i] in self.tracked_faces:
                        direct_similarity = cosine_similarity(
                            [face_encoding], 
                            [self.tracked_faces[ids[i]].encoding]
                        )[0][0]
                        
                        if direct_similarity > self.similarity_threshold:
                            print(f"Match found: {ids[i]}, similarity: {similarity}, direct: {direct_similarity}")
                            return ids[i]
            
            print("No match found above threshold")
            return None
            
        except Exception as e:
            # Fallback to direct comparison if ChromaDB query fails
            print(f"ChromaDB query error: {e}, falling back to direct comparison")
            
            # Use direct vector comparison
            best_match = None
            best_similarity = 0
            
            for face_id, face_vector in self.tracked_faces.items():
                similarity = cosine_similarity(
                    [face_encoding], 
                    [face_vector.encoding]
                )[0][0]
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = face_id
            
            if best_similarity > self.similarity_threshold:
                print(f"Direct match found: {best_match}, similarity: {best_similarity}")
                return best_match
            
            return None
    
    def add_or_update_face(self, face_encoding: np.ndarray, emotion: str, 
                          confidence: float, concentration: float, 
                          face_image: np.ndarray = None) -> str:
        """Add new face or update existing face with new detection"""
        current_time = datetime.now()
        
        # Check if this face already exists
        matching_face_id = self.find_matching_face(face_encoding)
        
        emotion_data = {
            'emotion': emotion,
            'confidence': confidence,
            'timestamp': current_time.isoformat()
        }
        
        if matching_face_id:
            print(f"Updating existing face: {matching_face_id}")
            # Update existing face
            face_vector = self.tracked_faces[matching_face_id]
            face_vector.last_seen = current_time
            face_vector.emotions.append(emotion_data)
            face_vector.concentration_scores.append(concentration)
            face_vector.total_detections += 1
            
            # Update in ChromaDB
            try:
                self.collection.update(
                    ids=[matching_face_id],
                    metadatas=[{
                        'last_seen': current_time.isoformat(),
                        'total_detections': face_vector.total_detections,
                        'avg_concentration': np.mean(face_vector.concentration_scores),
                        'dominant_emotion': max(set([e['emotion'] for e in face_vector.emotions]), 
                                              key=[e['emotion'] for e in face_vector.emotions].count)
                    }]
                )
            except Exception as e:
                print(f"Error updating face in ChromaDB: {e}")
            
            return matching_face_id
        else:
            print("Creating new face")
            # Create new face
            face_id = str(uuid.uuid4())
            face_vector = FaceVector(
                face_id=face_id,
                encoding=face_encoding,
                first_seen=current_time,
                last_seen=current_time,
                emotions=[emotion_data],
                concentration_scores=[concentration]
            )
            
            self.tracked_faces[face_id] = face_vector
            
            # Store in ChromaDB
            try:
                self.collection.add(
                    ids=[face_id],
                    embeddings=[face_encoding.tolist()],
                    metadatas=[{
                        'first_seen': current_time.isoformat(),
                        'last_seen': current_time.isoformat(),
                        'total_detections': 1,
                        'avg_concentration': concentration,
                        'dominant_emotion': emotion
                    }]
                )
            except Exception as e:
                print(f"Error adding face to ChromaDB: {e}")
            
            return face_id
    
    def get_all_faces(self) -> List[Dict]:
        """Get all tracked faces with their statistics"""
        return [face_vector.to_dict() for face_vector in self.tracked_faces.values()]
    
    def get_face_by_id(self, face_id: str) -> Optional[Dict]:
        """Get specific face by ID"""
        if face_id in self.tracked_faces:
            return self.tracked_faces[face_id].to_dict()
        return None
    
    def get_face_statistics(self) -> Dict:
        """Get overall statistics about all tracked faces"""
        if not self.tracked_faces:
            return {
                'total_faces': 0,
                'total_detections': 0,
                'avg_concentration': 0,
                'emotion_distribution': {}
            }
        
        total_faces = len(self.tracked_faces)
        total_detections = sum(face.total_detections for face in self.tracked_faces.values())
        all_concentrations = []
        all_emotions = []
        
        for face in self.tracked_faces.values():
            all_concentrations.extend(face.concentration_scores)
            all_emotions.extend([e['emotion'] for e in face.emotions])
        
        emotion_distribution = {}
        for emotion in all_emotions:
            emotion_distribution[emotion] = emotion_distribution.get(emotion, 0) + 1
        
        return {
            'total_faces': total_faces,
            'total_detections': total_detections,
            'avg_concentration': np.mean(all_concentrations) if all_concentrations else 0,
            'emotion_distribution': emotion_distribution
        }
    
    def save_to_json(self, filename: str = "face_tracking_data.json"):
        """Save all tracking data to JSON file"""
        data = {
            'faces': self.get_all_faces(),
            'statistics': self.get_face_statistics(),
            'saved_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
