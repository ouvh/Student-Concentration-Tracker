#!/usr/bin/env python3
"""
Test script for the enhanced YOLO-based device detector
"""
import cv2
import numpy as np
from device_detector import DeviceDetector
import time

def test_device_detection():
    """Test the device detection with webcam or sample image"""
    print("Initializing YOLO-based Device Detector...")
    detector = DeviceDetector()
    
    # Print model information
    model_info = detector.get_model_info()
    print(f"Model Info: {model_info}")
    print(f"Supported devices: {detector.get_supported_devices()}")
    
    # Test with webcam
    print("\nTesting with webcam (press 'q' to quit)...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    fps_counter = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect devices
        detection_result = detector.detect_devices_in_frame(frame)
        
        # Annotate frame
        annotated_frame = detector.annotate_frame_with_devices(frame, detection_result)
        
        # Display results
        cv2.imshow('YOLO Device Detection', annotated_frame)
        
        # Print detection info every 30 frames
        fps_counter += 1
        if fps_counter % 30 == 0:
            elapsed_time = time.time() - start_time
            fps = fps_counter / elapsed_time
            print(f"FPS: {fps:.2f} | Devices detected: {detection_result['total_devices']} | "
                  f"Distraction level: {detection_result['distraction_level']} | "
                  f"Method: {detection_result['detection_method']}")
            
            if detection_result['detected_devices']:
                print("Detected devices:")
                for device in detection_result['detected_devices']:
                    print(f"  - {device['type']}: {device['confidence']:.2f}")
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Print final statistics
    print(f"\nFinal Statistics:")
    stats = detector.get_device_statistics()
    print(f"Total detections: {stats['total_detections']}")
    print(f"Average devices per detection: {stats['avg_devices_per_detection']:.2f}")
    print(f"Peak device count: {stats['peak_device_count']}")
    print(f"Average distraction level: {stats['avg_distraction_level']}")
    print(f"Device type counts: {stats['device_type_counts']}")
    
    # Save test data
    if detector.save_device_data("test_device_data.json"):
        print("Test data saved to test_device_data.json")

def test_with_sample_image():
    """Test with a sample image if available"""
    print("\nTesting with sample image...")
    detector = DeviceDetector()
    
    # Create a sample image (white background)
    sample_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Add some text to indicate it's a test
    cv2.putText(sample_image, "Test Image - Place devices in camera view", 
                (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    # Detect devices
    detection_result = detector.detect_devices_in_frame(sample_image)
    
    # Annotate and display
    annotated_frame = detector.annotate_frame_with_devices(sample_image, detection_result)
    
    cv2.imshow('Test Image', annotated_frame)
    cv2.waitKey(3000)  # Show for 3 seconds
    cv2.destroyAllWindows()
    
    print(f"Sample image test completed. Detected {detection_result['total_devices']} devices.")

if __name__ == "__main__":
    print("=" * 50)
    print("YOLO-based Device Detector Test")
    print("=" * 50)
    
    try:
        test_device_detection()
        test_with_sample_image()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
