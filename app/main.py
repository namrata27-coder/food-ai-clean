from fastapi import FastAPI, UploadFile, File
from typing import List
import uuid
import os

from app.yolo_model import detect_items
from app.recipe_generator import generate_recipe
from fastapi.middleware.cors import CORSMiddleware


# from dotenv import load_dotenv
# load_dotenv()

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)



app = FastAPI(title="AI Food Recognition & Recipe API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/detect-and-generate")
async def detect_and_generate(images: List[UploadFile] = File(...)):
    all_items = set()

    for image in images:
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        detected = detect_items(file_path)
        all_items.update(detected)

    recipe = generate_recipe(list(all_items))

    return {
        "detected_items": list(all_items),
        "recipe": recipe
    }
