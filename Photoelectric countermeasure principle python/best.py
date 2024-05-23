from ultralytics import YOLO
import cv2
from ultralytics.trackers.utils.kalman_filter import KalmanFilterXYWH

model = YOLO(r'D:\1homework\digital image processing\d3dshot\yolov8n.pt')
video_path = 'test.mp4'  # 替换视频文件路径

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

FPS = 1000 // 24

# 用于存储每个人轨迹和卡尔曼滤波器的字典
trajectories = {}
kf_dict = {}
state_dict = {}
covariance_dict = {}
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
                width = int(x2 - x1)
                height = int(y2 - y1)

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
                    kf_dict[assigned_id] = KalmanFilterXYWH()
                    # 初始化状态和协方差矩阵
                    state, covariance = kf_dict[assigned_id].initiate([center_x, center_y, width, height])
                    state_dict[assigned_id] = state
                    covariance_dict[assigned_id] = covariance
                
                # 更新轨迹
                trajectories[assigned_id]['path'].append((center_x, center_y))
                # 限制轨迹长度
                if len(trajectories[assigned_id]['path']) > 5:
                    trajectories[assigned_id]['path'] = [(center_x, center_y)]
                # 使用卡尔曼滤波器进行预测
                kf = kf_dict[assigned_id]
                measurement = [center_x, center_y, width, height]
                state, covariance = kf.update(state_dict[assigned_id], covariance_dict[assigned_id], measurement)
                state_dict[assigned_id], covariance_dict[assigned_id] = kf.predict(state, covariance)
                predicted_x, predicted_y = int(state[0]), int(state[1])
                
                # 画当前的位置和预测的位置
                cv2.circle(annotated_frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.circle(annotated_frame, (predicted_x, predicted_y), 20, (0, 0, 255), 4)

                # 预测未来三次的位置
                future_positions = []
                future_state = state
                future_covariance = covariance
                for _ in range(3):
                    future_state, future_covariance = kf.predict(future_state, future_covariance)
                    future_positions.append((int(future_state[0]), int(future_state[1])))

                # 画未来三次预测的位置
                for pos in future_positions:
                    cv2.circle(annotated_frame, pos, 10, (0, 255, 255), 2)
    
    # 画每个人的实际轨迹线
    #for person_id, data in trajectories.items():
        #for j in range(1, len(data['path'])):
            #cv2.line(annotated_frame, data['path'][j - 1], data['path'][j], (0, 255, 0), 2)
    cv2.imshow('YOLOv8 Detection', annotated_frame)
    if cv2.waitKey(FPS) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
