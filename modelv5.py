import argparse
import os
import sys
from datetime import datetime
import numpy as np
import torch
from pathlib import Path
import time

sys.path.append(os.path.abspath("D:/NVTM/yolov5"))

from models.common import DetectMultiBackend
from utils.dataloaders import LoadImages
from utils.general import non_max_suppression, scale_boxes, check_img_size
from utils.torch_utils import select_device


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
def run(weights, source, savedir, imgsz=640, conf_thres=0.25, iou_thres=0.45):
    # Bắt đầu đo thời gian
    start_time = time.time()
    
    # Tạo timestamp cho session này
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    device = select_device('')
    model = DetectMultiBackend(weights, device=device)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)

    # Thư mục giống YOLOv8 (không thêm 'predict')
    save_dir = savedir
    labels_dir = os.path.join(save_dir, 'labels')
    os.makedirs(labels_dir, exist_ok=True)

    class_ids_all = []

    for path, img, im0s, vid_cap, s in dataset:
        img = torch.from_numpy(img).to(device).float() / 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img)
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0s.shape).round()

                # Tạo tên file với timestamp: <tên_ảnh>_<timestamp>.txt
                original_name = Path(path).stem
                label_filename = f"{original_name}_{timestamp}.txt"
                label_path = os.path.join(labels_dir, label_filename)
                
                with open(label_path, 'w') as f:
                    for *xyxy, conf, cls in det:
                        x_center = (xyxy[0] + xyxy[2]) / 2 / im0s.shape[1]
                        y_center = (xyxy[1] + xyxy[3]) / 2 / im0s.shape[0]
                        w = (xyxy[2] - xyxy[0]) / im0s.shape[1]
                        h = (xyxy[3] - xyxy[1]) / im0s.shape[0]
                        f.write(f"{int(cls)} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
                        class_ids_all.append(int(cls))

    # Kết thúc đo thời gian
    end_time = time.time()
    inference_duration = end_time - start_time

    write_inference_log(source, save_dir, class_ids_all, names, inference_duration, timestamp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, required=True)
    parser.add_argument('--image', type=str, required=True)
    parser.add_argument('--savedir', type=str, default='results')

    args = parser.parse_args()
    run(args.weights, args.image, args.savedir)
