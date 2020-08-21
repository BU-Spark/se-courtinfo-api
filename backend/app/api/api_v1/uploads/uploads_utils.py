from fastapi import UploadFile, File, HTTPException
from typing import List
import shutil
import uuid
import os.path
from pathlib import Path

ACCEPTED_FILE_FORMATS: List[str] = ["image/jpeg", "image/png", "application/pdf"]
WRITE_BUFFER_SIZE = 100
# Relative path
TEMP_FILE_PATH = 'uploaded_files/'


def verify_uploaded_file_type(file: UploadFile = File(...)):
    """
    Verifies the passed UploadFile complies with the restrictions specified.
    Throws 400 error if file does not conform
    :param file: UploadFile from request body
    :type file: UploadFile
    :return: None
    :rtype: None
    """
    if file is None or file.content_type not in ACCEPTED_FILE_FORMATS:
        raise HTTPException(status_code=400, detail="Bad uploaded file format")


# Taken from https://github.com/tiangolo/fastapi/issues/426#issuecomment-542828790
def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """
    Takes an FastAPI UploadFile and saves it to the specified destination
    :param upload_file: File to be saved
    :type upload_file: UploadFile
    :param destination: Relative path with name to save file
    :type destination: Path
    :return: Nothing
    :rtype: None
    """
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer, WRITE_BUFFER_SIZE)
    finally:
        upload_file.file.close()


def handle_upload_file(upload_file: UploadFile) -> Path:
    """
    Handles accepting the uploaded file, renaming and saving to temp storage for
    processing
    :param upload_file: Uploaded file from request body
    :type upload_file: FastAPi UploadFile
    :return: Relative path to file(with file name)
    :rtype: os.Path object
    """
    file_name = uuid.uuid4().hex + Path(upload_file.filename).suffix
    file_path = Path(os.path.join(TEMP_FILE_PATH, file_name))
    save_upload_file(upload_file, file_path)

    return file_path
