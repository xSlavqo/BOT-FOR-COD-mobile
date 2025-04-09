# train_yolo_build.py
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # lub yolov8s.pt / yolov8m.pt
model.train(
    data="yolo_dataset_builder/data.yaml",
    epochs=60,
    imgsz=640,
    batch=8
)
