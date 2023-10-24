from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic.types import UUID4
from app.db.session import get_db
from app.core.auth import get_current_active_superuser


ddi_record_router = d = APIRouter()

# @d.get('/ddi/all', response_model=List[DefendantDemoInfoBaseV1], response_model_exclude_none=True)
# def ddi_list(
#         skip: Optional[int] = Query(0, title="Query offset amount"),
#         limit: Optional[int] = Query(100, le=250, title="Number of results returned"),
#         db=Depends(get_db)
# ):
#     """
#     Get all ddi records Supports pagination through query parameters
#     """
#     ddis = get_all_ddi(db, skip=skip, limit=limit)
#     return ddis
#
# @d.post("/ddi/create")
# def create_ddi(
#     model: DefendantDemoInfoBaseV1,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     create the record
#     """
#     ddi = create_ddi(db, model)
#     return ddi.ddi_id
#
# @d.get("/ddi/{ddi_id}", response_model=DefendantDemoInfoBaseV1, response_model_exclude_none=True,)
# async def get_ddi_details(
#     ddi_id: UUID4,
#     db=Depends(get_db)
# ):
#     """
#     Get any ddi record by ddi id
#     """
#     ddi = get_ddi(db, ddi_id)
#     return ddi
#
# @d.post("/ddi/update")
# def create_ddi(
#     model: DefendantDemoInfoBaseV1,
#     db=Depends(get_db),
#     current_user=Depends(get_current_active_superuser),
# ):
#     """
#     create the record
#     """
#     ddi = update_ddi(db, current_user.id, model)
#     return ddi.ddi_id

