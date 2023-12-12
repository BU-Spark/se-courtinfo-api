from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, BackgroundTasks
from pydantic.types import UUID4
from pydantic import BaseModel, UUID4, ByteSize
import logging

from app.api.api_v1.uploads.uploads_utils import handle_upload_files
from app.ocr_sys_v2.ocr_read import read_text
from app.api.api_v1.bg_task import process_images_background
from app.core.auth import get_current_active_user, get_current_active_superuser

uploads_router = u = APIRouter()

# The upload feature verifies the type of the files and pass the files to read_text function one by one. 
@u.post(
    "/upload",
    # dependencies = [Depends(verify_uploaded_file_type)],
    responses = {400: {"description": "Returned when the uploaded file does not match the valid params"}}
)
def upload_form(
    files: list[UploadFile],
    form_type: int = Form(),
):
    print("call upload function")
    paths = handle_upload_files(files)
    for path in paths:
        print("Reading texts")
        s = read_text(str(path))
        print(s)

    return {"status": "succeeded",  "form_type": form_type, "urlSource": paths}
