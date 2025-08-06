import argparse
import os
from datetime import datetime
import numpy as np
import torch
from pathlib import Path
import time
from ultralytics import YOLO
import cv2

# Ghi log giống YOLOv8
def write_inference_log(image_path, save_dir, class_ids, names, inference_duration, timestamp):
    logs_dir = os.path.join(save_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"log_{timestamp}.txt")

    log_lines = [
        "=== Inference Log ===",
        f"Inference time: {datetime.now()}",
        f"Input: {image_path}",
        f"Inference duration: {inference_duration:.4f} seconds",
        f"Saved to: {os.path.join(save_dir, 'labels')}"
    ]

    if class_ids:
        log_lines.append("Classes detected:")
        for cls_id in sorted(set(class_ids)):
            log_lines.append(f"- {names[int(cls_id)]}")
    else:
        log_lines.append("No objects detected.")

    with open(log_path, 'w', encoding='utf-8') as f:
        for line in log_lines:
            f.write(f"{line}\n")

    print(log_path.strip())  # Cho server.js lấy log

# Inference
def run(weights, source, savedir, imgsz=640, conf=0.25):
    # Bắt đầu đo thời gian
    start_time = time.time()
    
    # Tạo timestamp cho session này
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    model = YOLO(weights)
    
    # Thư mục giống YOLOv8 (không thêm 'predict')
    save_dir = savedir
    labels_dir = os.path.join(save_dir, 'labels')
    predict_dir = os.path.join(save_dir, 'predict')
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(predict_dir, exist_ok=True)

    class_ids_all = []
    
    # Load ảnh
    img = cv2.imread(source)
    if img is None:
        print(f"Không thể đọc ảnh: {source}")
        return
    
    # Chạy inference
    results = model(source, imgsz=imgsz, conf=conf)
    
    for result in results:
        # Tạo tên file với timestamp
        original_name = Path(source).stem
        original_ext = Path(source).suffix
        
        # Tên file label với timestamp
        label_filename = f"{original_name}_{timestamp}.txt"
        label_path = os.path.join(labels_dir, label_filename)
        
        # Tên file ảnh kết quả với timestamp  
        result_img_filename = f"{original_name}_{timestamp}{original_ext}"
        result_img_path = os.path.join(predict_dir, result_img_filename)
        
        # Ghi file label
        with open(label_path, 'w') as f:
            if result.boxes is not None:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    conf_score = float(box.conf[0])
                    x_center, y_center, width, height = box.xywhn[0]
                    f.write(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
                    class_ids_all.append(cls)
        
        # Lưu ảnh kết quả với bounding boxes
        annotated_img = result.plot()
        cv2.imwrite(result_img_path, annotated_img)
        
        # Đồng thời copy ảnh gốc với tên cũ để server.js vẫn tìm thấy
        original_result_path = os.path.join(predict_dir, Path(source).name)
        cv2.imwrite(original_result_path, annotated_img)

    # Kết thúc đo thời gian
    end_time = time.time()
    inference_duration = end_time - start_time

    write_inference_log(source, save_dir, class_ids_all, model.names, inference_duration, timestamp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, required=True)
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--savedir', type=str, default='results')

    args = parser.parse_args()
    run(args.weights, args.image, args.savedir)
