from ultralytics import YOLO
from pathlib import Path
import cv2

MODEL_PATH = Path("models/food_small_best.pt")

model = YOLO(MODEL_PATH.as_posix())

def detect_items(image_path: str):
    results = model(image_path)
    items = set()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            items.add(model.names[cls_id])

    return list(items)
