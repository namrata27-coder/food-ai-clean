from fastapi import FastAPI, UploadFile, File
import uuid
import os

# from app.yolo_model import detect_items
# from app.recipe_generator import generate_recipe
from yolo_model import detect_items
from recipe_generator import generate_recipe


app = FastAPI(title="AI Food Recognition & Recipe API")

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/detect-and-generate")
async def detect_and_generate(image: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await image.read())

    items = detect_items(file_path)
    recipe = generate_recipe(items)

    return {
        "detected_items": items,
        "recipe": recipe
    }
