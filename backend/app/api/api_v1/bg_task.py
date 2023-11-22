from fastapi import BackgroundTasks, FastAPI
from typing import List
from pathlib import Path


app = FastAPI()

from app.ocr_sys_v2.ocr_read import read_text


def process_images_background(image_paths: List[Path], background_tasks: BackgroundTasks):
    # Queue the top-level function for each image as a background task
    for image_path in image_paths:
        background_tasks.add_task(read_text, image_path)

