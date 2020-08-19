from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.crud.cc_crud import get_all_cc, get_cc, get_cc_by_name
from app.db.session import get_db
from app.schemas.cc_schemas import CriminalComplaintOut, CriminalComplaint, CriminalComplaintCreate

ccf_record_router = r = APIRouter()


@r.get('/ccf/search', response_model=List[CriminalComplaintOut], response_model_exclude_none=True)
def search_ccf_by_name(
        name: str = Query(..., title="Name of defendant", max_length=50, min_length=2),
        limit: Optional[int] = Query(25, le=100, title="Number of results returned"),
        db=Depends(get_db)
):
    results = get_cc_by_name(db, name, limit)
    return results


@r.get('/ccf', response_model=List[CriminalComplaintOut], response_model_exclude_none=True)
def ccf_list(
        skip: Optional[int] = Query(0, title="Query offset amount"),
        limit: Optional[int] = Query(100, le=250, title="Number of results returned"),
        db=Depends(get_db)
):
    """
    Get all criminal complaint forms. Supports pagination through query parameters
    """
    ccfs = get_all_cc(db, skip=skip, limit=limit)
    return ccfs


@r.get('/ccf/{cc_id}', response_model=CriminalComplaintOut, response_model_exclude_none=True)
def get_single_ccf(
        cc_id: int,
        db=Depends(get_db)
):
    """
    Get a single Criminal Complaint Form based on the ID
    """
    ccf = get_cc(db, cc_id)
    return ccf
