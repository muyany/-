from ultralytics import YOLO
import cv2
from kalmanfilter import KalmanFilter

# 加载YOLOv8模型
model = YOLO(r'D:\1homework\digital image processing\d3dshot\yolov8n.pt')
video_path = 'test.mp4'  # 替换视频文件路径

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

FPS = 1000 // 10

# 用于存储每个人轨迹和卡尔曼滤波器的字典
trajectories = {}
predicted_trajectories = {}
kf_dict = {}
next_person_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (2560, 1600))
    results = model.predict(frame, show=False, classes=[0], verbose=False)
    annotated_frame = results[0].plot()
    
    # 当前帧检测到的所有人的中心点列表
    current_centers = []

    for result in results:
        if len(result.boxes.xyxy) != 0:
            for box in result.boxes.xyxy:
                thehead_tensor = box[0:4]
                thehead_tensor = thehead_tensor.cpu()
                thehead_numpy = thehead_tensor.numpy()
                x1, y1, x2, y2 = thehead_numpy
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # 添加到当前帧的中心点列表
                current_centers.append((center_x, center_y))

                # 为每个检测到的人分配一个唯一的ID
                assigned_id = None
                for person_id, data in trajectories.items():
                    if len(data['path']) > 0 and abs(data['path'][-1][0] - center_x) < 50 and abs(data['path'][-1][1] - center_y) < 50:
                        assigned_id = person_id
                        break
                
                if assigned_id is None:
                    assigned_id = next_person_id
                    next_person_id += 1
                    trajectories[assigned_id] = {'path': []}
                    predicted_trajectories[assigned_id] = {'path': []}
                    kf_dict[assigned_id] = KalmanFilter()
                
                # 更新轨迹
                trajectories[assigned_id]['path'].append((center_x, center_y))

                # 使用卡尔曼滤波器进行预测
                kf = kf_dict[assigned_id]
                predicted = kf.predict(center_x, center_y)

                # 更新预测轨迹
                predicted_trajectories[assigned_id]['path'].append(predicted)

                # 只保留一定长度的轨迹
                if len(trajectories[assigned_id]['path']) > 5:
                    trajectories[assigned_id]['path'].pop(0)
                if len(predicted_trajectories[assigned_id]['path']) > 10:
                    predicted_trajectories[assigned_id]['path'].pop(0)

                # 画当前的位置和预测的位置
                cv2.circle(annotated_frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.circle(annotated_frame, (predicted[0], predicted[1]), 20, (0, 0, 255), 4)

    # 画每个人的实际轨迹线
    for person_id, data in trajectories.items():
        for j in range(1, len(data['path'])):
            cv2.line(annotated_frame, data['path'][j - 1], data['path'][j], (0, 255, 0), 2)

    # 画每个人的预测轨迹线
    for person_id, data in predicted_trajectories.items(): 
        for j in range(1, len(data['path'])):
            cv2.line(annotated_frame, data['path'][j - 1], data['path'][j], (255, 0, 0), 2)

    cv2.imshow('YOLOv8 Detection', annotated_frame)
    if cv2.waitKey(FPS) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
