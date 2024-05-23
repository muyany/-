from ultralytics import YOLO
import cv2
from kalmanfilter import KalmanFilter

model = YOLO('yolov8n.pt')
video_path = 'test.mp4'

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

kf = KalmanFilter()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (640, 480))  # Resize frame to match model input
    results = model.predict(frame)
    annotated_frame = frame.copy()
    
    for detection in results:
        x, y, w, h = detection['bbox']
        x_center = x + w / 2
        y_center = y + h / 2
        predicted = kf.predict(x_center, y_center)
        cv2.circle(annotated_frame, (int(predicted[0]), int(predicted[1])), 10, (0, 255, 0), 2)
        cv2.circle(annotated_frame, (int(x_center), int(y_center)), 10, (255, 0, 0), 2)

    cv2.imshow('YOLOv8 Detection', annotated_frame)
    if cv2.waitKey(40) == ord('q'):  # Adjust FPS based on actual video framerate
        break

cap.release()
cv2.destroyAllWindows()
