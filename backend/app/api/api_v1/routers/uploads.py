from app.schemas.ddi_schemas import DefendantDemoInfoBaseV1
from app.db.session import get_db
from fastapi import APIRouter, Depends, File, UploadFile, Request
from pydantic.types import UUID4
from app.api.api_v1.uploads.uploads_utils import handle_upload_file
from app.api.api_v1.uploads.uploads_utils import verify_uploaded_file_type
from app.document_ai.process import process_ddi_document
from app.crud.ddi_crud import (
    create_ddi,
    get_ddi
)
uploads_router = u = APIRouter()

from app.core.auth import get_current_active_superuser
# Currently commented out since it uses the old OCR pipeline

# @u.post(
#     "/ccf",
#     dependencies=[Depends(verify_uploaded_file_type)],
#     responses={400: {"description": "Returned when the uploaded file does not match the valid params"}},
# )
# def upload_criminal_complaint(
#         file: UploadFile = File(...),
#         current_user: User = Depends(get_current_user),
# ):
#     """
#     Upload a Criminal Complaint Form via HTTP form
#     \n
#     Upload size is limited to 25MB and type must be, pdf, jpg, or png

#     :return Returns a task_id which can be used to track the status of the submission, check for errors etc.
#     see the /tasks route for details on how to lookup the status using the returned ID.
#     """
#     path = handle_upload_file(file)
#     string_path = str(path)
#     res = handle_criminal_complaint_task.apply_async(args=(string_path, current_user.id, "test", config.S3_BUCKET_NAME))
#     return {"job id": res.task_id}

@u.post(
    "/ddi",
    dependencies=[Depends(verify_uploaded_file_type)],
)
def upload_ddi_google(
    file: UploadFile = File(...),
):
    """
    Upload a Defendant Demographic Information Form via HTTP form and send to Google DocumentAI API
    \n
    Upload size is limited to 25MB and type must be, pdf, jpg, or png
    """
    path = handle_upload_file(file)
    string_path = str(path)
    ddi = process_ddi_document(string_path, file.content_type)
    return ddi

@u.post("/ddi/modify")
def modify_ddi_google(
    request: Request,
    model: DefendantDemoInfoBaseV1,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    ddi = create_ddi(db, model)
    return ddi.ddi_id

@u.get(
    "/ddi/{ddi_id}", response_model=DefendantDemoInfoBaseV1, response_model_exclude_none=True,
)
async def get_ddi_details(
    request: Request,
    ddi_id: UUID4,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    ddi = get_ddi(db, ddi_id)
    return ddi
    # return encoders.jsonable_encoder(
    #     ddi, skip_defaults=True, exclude_none=True,
    # )
