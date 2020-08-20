import os

from celery.exceptions import Ignore
from fastapi import Depends
from pydantic.types import UUID4

from app.aws.s3_client import upload_file_to_s3, get_s3_client
from app.celery_system.task_classes import TaskStates, TaskTypes
from app.crud.cc_crud import create_cc
from app.db.session import SessionLocal
from app.ocr_system.processor.criminal_complaint import extract_criminal_complaint
from app.ocr_system.processor.text_extractor import extract_document_text
from app.ocr_system.verifiers.form_validators import verify_cc
from app.schemas.cc_schemas import CriminalComplaintBase, CriminalComplaintCreate


def pipeline_criminal_complaint_form(task, image_path: str, current_user_id: UUID4, aws_obj_prefix: str,
                                     aws_bucket: str, s3_client=get_s3_client()):
    """
    Wrapper function that handles the entire OCR pipeline from loading a file to processing
    and then returning the result of the OCR to the Celery backend.
    """
    try:
        task.update_state(state=TaskStates.STARTING)
        text = extract_document_text(image_path)
        unsafe_cc = CriminalComplaintBase(**extract_criminal_complaint(text).dict())
        safe_cc = verify_cc(unsafe_cc)
        if safe_cc is None:
            task.update_state(state=TaskStates.OCR_FAILURE)
            raise Ignore()
        (res, img_key) = upload_file_to_s3(s3_client, image_path, aws_obj_prefix, aws_bucket)
        if not res:
            task.update_state(state=TaskStates.AWS_FAILURE)
            # Cleanup temp files, we want to remove the file regardless of success
            raise Ignore()
        full_cc = CriminalComplaintCreate(**safe_cc.dict(), created_by=current_user_id, aws_bucket=aws_bucket,
                                          img_key=img_key)
        db = SessionLocal()
        db_cc = create_cc(db, full_cc)
        task.update_state(state=TaskStates.SUCCESS)
    finally:
        # Cleanup the temp image no matter what happens. Otherwise
        # we will overload the system with temp files.
        os.remove(image_path)

    return {'id': db_cc.cc_id, 'type': TaskTypes.CCF}
