import pickle

from celery import states
from fastapi import APIRouter, Depends, HTTPException
from pydantic.types import UUID4
from starlette.types import Message

from app.crud.celery_crud import get_task_status
from app.db.session import get_db

task_router = t = APIRouter()


@t.get('/tasks/{task_id}', responses={404: {}})
def task_details(
        task_id: UUID4,
        db=Depends(get_db),
):
    """
    Check the status of a task submitted via one of the upload routes.
    :returns The current status of the task and possible results(could be nil)
    """
    db_task = get_task_status(db, str(task_id))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task ID not found")
    # Due to an error in the Celery code results are stored in the backend as pickles
    # regardless of the serializer chosen(JSON is the default). That is why we must
    # unpickle the result before returning(Pydantic does not support pickles)
    # https://github.com/celery/celery/pull/5907
    # Check to make sure the result exists before unpickling
    if db_task.result:
        raw_result = pickle.loads(db_task.result)
    else:
        raw_result = None

    # Since we adopt Celery's backend structure we need to check for failure of the task.
    # In the case there is a failure Celery will include that data(the exception etc) as a result of the function
    # this should not be returned to the client so we clear it out here if needed
    if db_task.status == states.FAILURE:
        raw_result = None
    return {'celery_id': task_id, 'task_state': db_task.status, 'db_obj': raw_result}
