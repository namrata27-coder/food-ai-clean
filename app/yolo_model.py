from ultralytics import YOLO
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "food_small_best.pt"

model = YOLO(str(MODEL_PATH))

def detect_items(image_path: str):
    results = model(image_path)
    items = set()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            items.add(model.names[cls_id])

    return list(items)
