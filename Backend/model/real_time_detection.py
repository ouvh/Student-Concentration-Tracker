import cv2
import numpy as np
from keras.models import load_model
from datetime import datetime
from detection_results_saver_v2 import DetectionResultsSaverV2

IMG_SIZE = (48, 48)

def calculate_concentration(prediction, emotion_labels):
    """
    Calculate concentration score based on emotion predictions.
    This is a sample heuristic: higher concentration for neutral and happy emotions,
    lower for negative emotions.
    """
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
    for i, emotion in enumerate(emotion_labels):
        weight = concentration_weights.get(emotion, 0.5)
        concentration += prediction[i] * weight
    return concentration * 100  # scale to percentage

import time

def real_time_emotion_detection(duration=10):#time selection (duration = '' )
    # Load the saved model
    model = load_model("best_vgg16_improved_model.keras")

    # Emotion labels - these should match the order used in training
    emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

    # Load OpenCV face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)

    start_time = time.time()
    concentration_sum = 0.0
    frame_count = 0
    avg_concentration = 0.0

    # Initialize detection results saver
    saver = DetectionResultsSaverV2()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, IMG_SIZE)
            face_img = face_img.astype('float32') / 255
            face_img = np.expand_dims(face_img, axis=0)

            prediction = model.predict(face_img)[0]
            max_index = int(np.argmax(prediction))
            emotion = emotion_labels[max_index]
            confidence = prediction[max_index] * 100  # percentage

            concentration = calculate_concentration(prediction, emotion_labels)

            concentration_sum += concentration
            frame_count += 1

            avg_concentration = concentration_sum / frame_count if frame_count > 0 else 0

            # Save detection result with timestamp and bounding box
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            saver.add_result(timestamp, emotion, confidence, concentration, x, y, w, h)

            # print(f"Detected emotion: {emotion} with confidence: {confidence:.2f}%")
            # print(f"Concentration score: {concentration:.2f}%")
            # print(f"Average concentration over {frame_count} frames: {avg_concentration:.2f}%")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            label = f"{emotion}: {confidence:.2f}%"
            concentration_label = f"Concentration: {concentration:.2f}%"
            avg_concentration_label = f"Avg Conc ({frame_count} frames): {avg_concentration:.2f}%"
            cv2.putText(frame, label, (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            cv2.putText(frame, concentration_label, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
            cv2.putText(frame, avg_concentration_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,200,200), 2)

        cv2.imshow('Real-time Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            print(f"Average concentration over {duration} seconds: {avg_concentration:.2f}%")
            break
            # Reset counters for next duration period
            start_time = time.time()
            concentration_sum = 0.0
            frame_count = 0

    # Save all results to Excel after loop ends
    saver.save_to_excel()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_emotion_detection()
