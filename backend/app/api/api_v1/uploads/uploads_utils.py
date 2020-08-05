from fastapi import UploadFile, File, HTTPException
from typing import List
import shutil
import uuid
import os.path
from pathlib import Path

ACCEPTED_FILE_FORMATS: List[str] = ["image/jpeg", "image/png", "application/pdf"]
WRITE_BUFFER_SIZE = 100
TEMP_FILE_PATH = 'uploaded_files/'
'''
Checks an uploaded file for type restrictions using the MIME type

:param file: File to be verified, normally an UploadedFile
'''


def verify_uploaded_file_type(
        file: UploadFile = File(...),
):
    if file is not None and file.content_type not in ACCEPTED_FILE_FORMATS:
        raise HTTPException(status_code=400, detail="Bad uploaded file format")


# Taken from https://github.com/tiangolo/fastapi/issues/426#issuecomment-542828790
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer, WRITE_BUFFER_SIZE)
    finally:
        upload_file.file.close()


def handle_upload_file(upload_file: UploadFile) -> Path:
    file_name = uuid.uuid4().hex + Path(upload_file.filename).suffix
    file_path = Path(os.path.join(TEMP_FILE_PATH, file_name))
    save_upload_file(upload_file, file_path)
    return file_path
