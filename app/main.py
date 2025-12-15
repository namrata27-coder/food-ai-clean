from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List
import uuid
import os

from dotenv import load_dotenv
load_dotenv()  # loads .env from app/

from app.yolo_model import detect_items
from app.recipe_generator import generate_recipe

# -------------------------
# App setup
# -------------------------


app = FastAPI(title="AI Food Recognition & Recipe API")

@app.get("/__debug__")
async def debug():
    return {"status": "THIS MAIN.PY IS RUNNING"}


# -------------------------
# CORS (required for phone browsers)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Temp upload directory
# -------------------------
BASE_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Home page (HTML upload UI)
# -------------------------
@app.get("/home", response_class=HTMLResponse)
async def home():
    html_path = os.path.join(BASE_DIR, "upload.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

# -------------------------
# Detect + generate recipe
# -------------------------
@app.post("/detect-and-generate")
async def detect_and_generate(images: List[UploadFile] = File(...)):
    all_items = set()

    for image in images:
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        detected_items = detect_items(file_path)
        all_items.update(detected_items)

    recipe = generate_recipe(list(all_items))

    return {
        "detected_items": list(all_items),
        "recipe": recipe
    }
