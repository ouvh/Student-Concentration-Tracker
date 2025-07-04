# Enhanced YOLO-based Device Detection

## Overview
The device detector has been upgraded to use state-of-the-art YOLOv8 model for accurate real-time device detection. This provides significant improvements over the previous contour-based detection method.

## Key Features

### 1. **YOLOv8 Integration**
- Uses YOLOv8 nano model for fast and accurate object detection
- Automatically downloads the model on first use
- Fallback to simple contour detection if YOLO is unavailable

### 2. **Enhanced Device Detection**
- **Smartphones**: High distraction weight (4)
- **Tablets**: High distraction weight (3)
- **Laptops**: Medium distraction weight (1) - considered work device
- **Monitors**: Low distraction weight (0.5) - work-related
- **Books**: Negative distraction weight (-1) - educational benefit
- **Peripherals**: Mouse, keyboard (0.2) - work tools
- **Entertainment**: Remote control (2) - moderate distraction

### 3. **Advanced Features**
- **Confidence-based detection**: Adjustable confidence threshold
- **Multiple device categories**: Expanded from 6 to 12+ device types
- **Enhanced annotation**: Better visual feedback with color coding
- **Performance monitoring**: FPS tracking and detection method reporting
- **Smart classification**: Maps COCO dataset classes to custom categories

## Installation

### Method 1: Automatic Setup (Recommended)
```bash
# Run the setup script
setup_yolo.bat
```

### Method 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install ultralytics torch torchvision opencv-python numpy
```

## Usage

### Basic Usage
```python
from device_detector import DeviceDetector

# Initialize detector
detector = DeviceDetector()

# Get model information
model_info = detector.get_model_info()
print(f"Using: {model_info['model_type']}")

# Detect devices in frame
detection_result = detector.detect_devices_in_frame(frame)

# Annotate frame
annotated_frame = detector.annotate_frame_with_devices(frame, detection_result)
```

### Advanced Configuration
```python
# Set detection confidence (0.1 to 0.9)
detector.set_detection_confidence(0.4)

# Get supported device types
supported_devices = detector.get_supported_devices()

# Get detection statistics
stats = detector.get_device_statistics()
```

## Testing

### Quick Test
```bash
python test_yolo_detection.py
```

### Integration Test
```bash
python main.py
# Then access the frontend to see live detection
```

## Performance Optimization

### Model Variants
- **YOLOv8n**: Fastest, good accuracy (default)
- **YOLOv8s**: Balanced speed/accuracy
- **YOLOv8m**: Better accuracy, slower
- **YOLOv8l**: High accuracy, much slower
- **YOLOv8x**: Best accuracy, slowest

To change model variant, modify the initialization:
```python
self.yolo_model = YOLO('yolov8s.pt')  # Use small model
```

### Confidence Tuning
- **0.3**: Default, good balance
- **0.2**: More detections, some false positives
- **0.5**: Fewer detections, higher precision

## Distraction Level Calculation

The enhanced system uses weighted scoring:

| Device Type | Weight | Reasoning |
|-------------|---------|-----------|
| Smartphone  | 4       | High distraction potential |
| Tablet      | 3       | High distraction potential |
| Remote      | 2       | Entertainment device |
| Laptop      | 1       | Work device, moderate |
| Monitor     | 0.5     | Work-related display |
| Mouse/Keyboard | 0.2  | Work peripherals |
| Book        | -1      | Educational benefit |

**Distraction Levels:**
- **Low**: Score ≤ 1 (Green)
- **Medium**: Score 1-3 (Yellow)  
- **High**: Score > 3 (Red)

## Troubleshooting

### Common Issues

1. **YOLO Import Error**
   ```
   Solution: Run setup_yolo.bat or pip install ultralytics
   ```

2. **Model Download Failed**
   ```
   Solution: Check internet connection, model will download automatically
   ```

3. **Low FPS Performance**
   ```
   Solution: Use YOLOv8n model, reduce frame processing frequency
   ```

4. **False Positives**
   ```
   Solution: Increase confidence threshold to 0.4-0.5
   ```

### Fallback Mode
If YOLO is unavailable, the system automatically falls back to the original contour-based detection method, ensuring continuous operation.

## API Endpoints

The enhanced detector integrates with existing API endpoints:

- `GET /api/devices/current` - Current device summary
- `GET /api/devices/statistics` - Enhanced statistics with method info
- `GET /api/devices/history` - Detection history with method tracking
- `POST /api/devices/clear-history` - Clear detection history

## Future Enhancements

1. **Custom Training**: Train YOLO on classroom-specific devices
2. **Temporal Tracking**: Track device usage patterns over time
3. **Student Association**: Link detected devices to specific students
4. **Attention Correlation**: Correlate device usage with concentration levels
5. **Smart Alerts**: Intelligent notifications based on usage patterns

## Technical Details

### Model Architecture
- **Framework**: YOLOv8 (Ultralytics)
- **Input Size**: 640x640 (auto-resized)
- **Classes**: 80 COCO classes, filtered to relevant devices
- **Inference Time**: ~10-30ms per frame (depends on hardware)

### Hardware Requirements
- **Minimum**: 4GB RAM, integrated graphics
- **Recommended**: 8GB+ RAM, dedicated GPU
- **Optimal**: 16GB+ RAM, CUDA-compatible GPU

### Dependencies
- **Core**: Python 3.8+, OpenCV, NumPy
- **AI**: PyTorch, Ultralytics YOLO
- **Vision**: Pillow, scikit-learn
- **Web**: FastAPI, WebSockets

## Contributing

To contribute to the enhanced device detection:

1. Fork the repository
2. Create a feature branch
3. Implement improvements
4. Add tests
5. Submit a pull request

## License

This enhanced device detection system is part of the Student Concentration Tracker project and follows the same licensing terms.
