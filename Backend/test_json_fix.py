#!/usr/bin/env python3
"""
Test script to verify JSON serialization fix for device detection
"""
import json
import numpy as np
from device_detector import DeviceDetector
import cv2

def test_json_serialization():
    """Test that device detection results are JSON serializable"""
    print("Testing JSON serialization fix...")
    
    # Initialize detector
    detector = DeviceDetector()
    
    # Create a test frame
    test_frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # Add some simple shapes to test detection
    cv2.rectangle(test_frame, (100, 100), (200, 300), (0, 0, 0), -1)  # Phone-like shape
    cv2.rectangle(test_frame, (300, 150), (500, 250), (0, 0, 0), -1)  # Laptop-like shape
    
    print("Created test frame with test shapes")
    
    # Detect devices
    try:
        detection_result = detector.detect_devices_in_frame(test_frame)
        print(f"Detection completed. Found {detection_result['total_devices']} devices")
        print(f"Detection method: {detection_result['detection_method']}")
        
        # Test JSON serialization
        json_string = json.dumps(detection_result, indent=2)
        print("✅ JSON serialization successful!")
        
        # Parse back to verify
        parsed_result = json.loads(json_string)
        print("✅ JSON parsing successful!")
        
        # Print some results
        print(f"\nDetection Results:")
        print(f"Total devices: {parsed_result['total_devices']}")
        print(f"Distraction level: {parsed_result['distraction_level']}")
        print(f"Device counts: {parsed_result['device_counts']}")
        
        if parsed_result['detected_devices']:
            print(f"\nDetected devices details:")
            for i, device in enumerate(parsed_result['detected_devices']):
                print(f"  Device {i+1}:")
                print(f"    Type: {device['type']}")
                print(f"    Confidence: {device['confidence']}")
                print(f"    Bbox: {device['bbox']}")
                print(f"    Area: {device['area']}")
                print(f"    Aspect ratio: {device['aspect_ratio']}")
        
        return True
        
    except TypeError as e:
        if "not JSON serializable" in str(e):
            print(f"❌ JSON serialization failed: {e}")
            return False
        else:
            raise e
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_websocket_simulation():
    """Simulate WebSocket data transmission"""
    print("\n" + "="*50)
    print("Testing WebSocket simulation...")
    
    detector = DeviceDetector()
    
    # Create test frame
    test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    try:
        # Get detection result
        detection_result = detector.detect_devices_in_frame(test_frame)
        
        # Simulate what happens in main.py WebSocket message
        message = {
            "type": "detection_update",
            "data": {
                "devices": detection_result,
                "statistics": detector.get_device_statistics()
            },
            "timestamp": detection_result['timestamp']
        }
        
        # Try to serialize the complete message
        json_message = json.dumps(message)
        print("✅ WebSocket message serialization successful!")
        
        # Test message size
        message_size = len(json_message)
        print(f"Message size: {message_size} bytes")
        
        if message_size > 1024 * 1024:  # 1MB
            print("⚠️  Warning: Message is quite large for WebSocket")
        else:
            print("✅ Message size is reasonable for WebSocket")
            
        return True
        
    except Exception as e:
        print(f"❌ WebSocket simulation failed: {e}")
        return False

def test_model_info():
    """Test model info serialization"""
    print("\n" + "="*50)
    print("Testing model info serialization...")
    
    detector = DeviceDetector()
    
    try:
        model_info = detector.get_model_info()
        json.dumps(model_info)
        print("✅ Model info serialization successful!")
        print(f"Model type: {model_info['model_type']}")
        print(f"Status: {model_info['status']}")
        
        statistics = detector.get_device_statistics()
        json.dumps(statistics)
        print("✅ Statistics serialization successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Model info serialization failed: {e}")
        return False

if __name__ == "__main__":
    print("JSON Serialization Test for Enhanced Device Detection")
    print("="*60)
    
    tests_passed = 0
    total_tests = 3
    
    # Run tests
    if test_json_serialization():
        tests_passed += 1
    
    if test_websocket_simulation():
        tests_passed += 1
        
    if test_model_info():
        tests_passed += 1
    
    # Results
    print("\n" + "="*60)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! JSON serialization issue is fixed.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    print("\nThe device detection should now work without JSON serialization errors.")
