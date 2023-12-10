from fastapi import BackgroundTasks, FastAPI
from typing import List
from pathlib import Path
import logging
from app.ocr_sys_v2.ocr_read import read_text


app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_images_background(image_paths: List[Path], background_tasks: BackgroundTasks):
    # Queue the top-level function for each image as a background task
    for image_path in image_paths:
        background_tasks.add_task(process_image, image_path)

def process_image(image_path: Path):
    try:
        # Call the read_text function
        result = read_text(image_path)

        # Log the result
        logger.info(f"Image processed: {image_path}, Result: {result}")
    except Exception as e:
        # Log any exceptions that occur during processing
        logger.error(f"Error processing image {image_path}: {e}")