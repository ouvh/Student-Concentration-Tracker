@echo off
echo Installing Enhanced Device Detection Dependencies...
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing core dependencies...
pip install fastapi uvicorn websockets python-multipart

echo.
echo Step 3: Installing computer vision dependencies...
pip install opencv-python numpy Pillow

echo.
echo Step 4: Installing YOLO and AI dependencies...
echo This may take a while as it downloads PyTorch and YOLOv8...
pip install ultralytics torch torchvision

echo.
echo Step 5: Installing face recognition dependencies...
pip install face-recognition tensorflow keras

echo.
echo Step 6: Installing data management dependencies...
pip install chromadb pandas scikit-learn

echo.
echo Step 7: Installing utilities...
pip install python-dateutil requests

echo.
echo Installation complete!
echo.
echo To test the enhanced device detection, run:
echo python test_yolo_detection.py
echo.
echo To start the server with enhanced device detection:
echo python main.py
pause
