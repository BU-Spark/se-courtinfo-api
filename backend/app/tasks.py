
from pydantic import UUID4

from app.celery_system.task_classes import TaskReturnValue
from app.core.celery_app import celery_app
from app.ocr_system.ocr_pipelines import pipeline_criminal_complaint_form


@celery_app.task(acks_late=True)
def example_task(word: str) -> str:
    return f"testing task returns {word}"


@celery_app.task(bind=True, acks_late=True)
def handle_criminal_complaint_task(self, image_path: str, current_user_id: UUID4, aws_obj_prefix: str,
                                   aws_bucket: str) -> TaskReturnValue:
    """
    Process a Criminal Complaint Form from image -> OCR -> DB. Uses custom states(that are not reported to Flower)
    to handle the different failure scenarios. The state can be checked using the Celery AsyncResult type via the ID provided
    at task start(from the caller).

    The file and it's contents are only saved in AWS and the DB if the OCR check passes
    :param self: The task itself
    :type self:
    :param image_path: The path to the image file to be processed
    :type image_path: str
    :param current_user_id: The user who made this request
    :type current_user_id: UUID4 -- Datebase ID
    :param aws_obj_prefix: Prefix for object placed in AWS
    :type aws_obj_prefix: str
    :param aws_bucket: Destination bucket for image
    :type aws_bucket: str
    :return: ID of object created in DB
    :rtype: int
    """
    results = pipeline_criminal_complaint_form(self, image_path, current_user_id, aws_obj_prefix, aws_bucket)
    return results
