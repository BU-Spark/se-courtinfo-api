from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from app.api.api_v1.uploads.uploads_utils import handle_upload_file
from app.api.api_v1.uploads.uploads_utils import verify_uploaded_file_type

uploads_router = u = APIRouter()


@u.post(
    "/ccf",
    dependencies=[Depends(verify_uploaded_file_type)],
    responses={400: {"description": "Returned when the uploaded file does not match the valid params"}},
)
def upload_criminal_complaint(
        file: UploadFile = File(...)
):
    """
    Upload a Criminal Complaint Form via HTTP form
    \n
    Upload size is limited to 25MB and type must be, pdf, jpg, or png
    """

    path = handle_upload_file(file)
    return {"uploaded": path}


@u.post(
    "/abf",
    dependencies=[Depends(verify_uploaded_file_type)],
    responses={400: {"description": "Returned when the uploaded file does not match the valid params"}},
)
def upload_arrest_booking_form(
        file: UploadFile = File(...)
):
    """
    Upload an arrest booking form
    :param upload: File being uploaded
    :type upload: formdata file
    :return: Name and path of uploaded ilfe
    :rtype: JSON
    """
    path = handle_upload_file(file)
    return {"uploaded": path}
