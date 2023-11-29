from fastapi import UploadFile, File, HTTPException
from typing import List
import shutil
import uuid
import os.path
from pathlib import Path

ACCEPTED_FILE_FORMATS: List[str] = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "application/pdf",
]
WRITE_BUFFER_SIZE = 100
# Relative path
TEMP_FILE_PATH = os.path.join(os.path.dirname(__file__), "uploaded_files")


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
        with destination.open("ab") as buffer:
            shutil.copyfileobj(upload_file.file, buffer, WRITE_BUFFER_SIZE)
    finally:
        upload_file.file.close()

def handle_upload_files(files: list[UploadFile]) -> List[Path]:
    """
    Handles accepting multiple uploaded files, renaming and saving to temp storage for
    processing
    """
    file_paths = []
    for file in files:
        file_name = uuid.uuid4().hex + Path(file.filename).suffix
        file_path = Path(TEMP_FILE_PATH).joinpath(file_name) 
        save_upload_file(file, file_path)
        file_paths.append(file_path)

    return file_paths if file_paths else None

# def get_uploaded_files_type(files: list[UploadFile] = list[File(...)]) -> ACCEPTED_FILE_FORMATS:
#     """
#     Verifies the passed UploadFile complies with the restrictions specified.
#     Throws 400 error if file does not conform
#     :param file: UploadFile from request body
#     :type file: UploadFile
#     :return: None
#     :rtype: None
#     """
#     if files[0] is None or files[0].content_type not in ACCEPTED_FILE_FORMATS:
#         raise HTTPException(status_code=400, detail="Bad uploaded file format")
#     else:
#         return files[0].content_type not in ACCEPTED_FILE_FORMATS


# Taken from https://github.com/tiangolo/fastapi/issues/426#issuecomment-542828790