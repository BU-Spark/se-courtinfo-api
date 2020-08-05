from pathlib import Path

from fastapi import APIRouter, Request, Depends, Response, encoders, File, UploadFile
import typing as t

from app.api.api_v1.uploads.uploads_utils import verify_uploaded_file_type
from app.core.celery_app import celery_app
from app.api.api_v1.uploads.uploads_utils import handle_upload_file

uploads_router = u = APIRouter()

@u.post(
    "/ccf",
    dependencies=[Depends(verify_uploaded_file_type)],
    responses={400: {"description": "Returned when the uploaded file does not match the valid params"}},
)
def upload_criminal_complaint(
    file: UploadFile = File(...),
):
    """
    Upload a Criminal Complaint Form via HTTP form
    \n
    Upload size is limited to 25MB and type must be, pdf, jpg, or png
    """
    
    path = handle_upload_file(file)
    return {"uploaded": path}


