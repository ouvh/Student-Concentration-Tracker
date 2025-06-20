import cv2
import numpy as np
import face_recognition
import time
import os
import argparse
from typing import List, Dict, Tuple

def analyze_face_detection(image_path: str = None, 
                          test_camera: bool = False,
                          show_visualization: bool = True,
                          detection_model: str = "hog",
                          upsamples: int = 1) -> Dict:
    """
    Analyze face detection performance and accuracy using different parameters.
    
    Args:
        image_path: Path to image file to analyze
        test_camera: If True, use webcam instead of image file
        show_visualization: If True, show visualization of detection
        detection_model: Model to use ("hog" or "cnn")
        upsamples: Number of times to upsample image (increases sensitivity but slows performance)
    
    Returns:
        Dict with detection results
    """
    print("\n--- Face Detection Diagnostic Tool ---")
    print(f"Detection model: {detection_model}")
    print(f"Upsamples: {upsamples}")
    
    if test_camera:
        print("Initializing camera...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return {"error": "Could not open camera"}
        
        print("Press 'q' to quit, 'c' to capture current frame for analysis")
        frame = None
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
                
            # Show live feed
            cv2.imshow("Camera Feed (Press 'c' to capture, 'q' to quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('c'):
                print("Frame captured for analysis")
                break
                
        cap.release()
        cv2.destroyAllWindows()
        
        if frame is None:
            return {"error": "No frame captured"}
            
        # Use the captured frame for analysis
        img = frame
    else:
        if not image_path or not os.path.exists(image_path):
            print("Error: Image file not found")
            return {"error": "Image file not found"}
            
        print(f"Reading image: {image_path}")
        img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not read image")
        return {"error": "Could not read image"}
        
    # Convert to RGB (face_recognition uses RGB)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Try different detection parameters and measure performance
    results = {}
    
    print("\nRunning face detection...")
    start_time = time.time()
    
    # Detect faces with the specified parameters
    face_locations = face_recognition.face_locations(
        rgb_img, 
        model=detection_model,
        number_of_times_to_upsample=upsamples
    )
    
    # Encode the detected faces
    face_encodings = face_recognition.face_encodings(
        rgb_img,
        face_locations,
        num_jitters=1
    )
    
    detection_time = time.time() - start_time
    
    # Collect results
    results = {
        "faces_detected": len(face_locations),
        "detection_time_seconds": detection_time,
        "model": detection_model,
        "upsamples": upsamples,
        "image_dimensions": img.shape,
        "face_locations": face_locations
    }
    
    print(f"Detection Results:")
    print(f"- Faces detected: {len(face_locations)}")
    print(f"- Detection time: {detection_time:.4f} seconds")
    
    # Visualize the results
    if show_visualization:
        # Create a copy to draw on
        output_img = img.copy()
        
        # Draw rectangles around faces
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Use different colors for different faces
            colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), 
                     (0, 255, 255), (255, 0, 255), (128, 128, 0), (0, 128, 128)]
            color = colors[i % len(colors)]
            
            # Draw rectangle
            cv2.rectangle(output_img, (left, top), (right, bottom), color, 2)
            
            # Add label
            cv2.putText(output_img, f"Face #{i+1}", (left, top - 10),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Add summary info on the image
        cv2.putText(output_img, f"Detected: {len(face_locations)} faces", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(output_img, f"Time: {detection_time:.4f}s", (10, 60),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(output_img, f"Model: {detection_model}, Upsamples: {upsamples}", (10, 90),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display the image
        cv2.imshow(f"Face Detection Results", output_img)
        print("Press any key to close the visualization...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Face Detection Diagnostic Tool')
    parser.add_argument('--image', type=str, help='Path to image file')
    parser.add_argument('--camera', action='store_true', help='Use camera instead of image file')
    parser.add_argument('--model', type=str, default='hog', choices=['hog', 'cnn'], 
                       help='Detection model (hog or cnn)')
    parser.add_argument('--upsamples', type=int, default=1, help='Number of times to upsample the image')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    
    args = parser.parse_args()
    
    if not args.image and not args.camera:
        print("Error: Either --image or --camera must be specified")
        parser.print_help()
        exit(1)
        
    analyze_face_detection(
        image_path=args.image,
        test_camera=args.camera,
        show_visualization=not args.no_viz,
        detection_model=args.model,
        upsamples=args.upsamples
    )
