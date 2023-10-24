from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, Path, Union

from app.aws.s3_client import get_s3_client, create_presigned_url
from app.crud.cc_crud import get_all_cc, get_cc, get_cc_by_name
from app.crud.ddi_crud import get_all_ddi, get_ddi, get_ddi_by_name
from app.db.session import get_db
from app.schemas.cc_schemas import CriminalComplaintOut
from app.schemas.ddi_schemas import DefendantDemoInfoCreate

record_router = r = APIRouter()


@r.get(
    "/{form_type}/search",
    response_model=List[Union[CriminalComplaintOut, DefendantDemoInfoCreate]],
    response_model_exclude_none=True,
)
def search_form_by_name(
    form_type: str = Path(..., title="Type of Form (ccf/ddi)"),
    name: str = Query(..., title="Name of defendant", max_length=50, min_length=2),
    limit: Optional[int] = Query(25, le=100, title="Number of results returned"),
    db=Depends(get_db),
):
    """
    Search for a form by name of defendant based on the form_type
    """
    if form_type == "ccf":
        results = get_cc_by_name(db, name, limit)
    elif form_type == "ddi":
        results = get_ddi_by_name(db, name, limit)
    else:
        return {"error": "Invalid form_type. Use 'ccd' or 'ddi'."}

    return results


@r.get(
    "/{form_type}}",
    response_model=List[Union[CriminalComplaintOut, DefendantDemoInfoCreate]],
    response_model_exclude_none=True,
)
def form_list(
    form_type: str = Path(..., title="Type of Form (ccf/ddi)"),
    skip: Optional[int] = Query(0, title="Query offset amount"),
    limit: Optional[int] = Query(100, le=250, title="Number of results returned"),
    db=Depends(get_db),
):
    """
    Get all forms with the chosen form type. Supports pagination through query parameters
    """
    if form_type == "ccf":
        results = get_all_cc(db, skip=skip, limit=limit)
    elif form_type == "ddi":
        results = get_all_ddi(db, skip=skip, limit=limit)
    else:
        return {"error": "Invalid form_type. Use 'ccd' or 'ddi'."}

    return results


@r.get(
    "/{form_type}/{id}",
    response_model=List[Union[CriminalComplaintOut, DefendantDemoInfoCreate]],
    response_model_exclude_none=True,
)
def get_single_form(
    id: int,
    db=Depends(get_db),
    form_type: str = Path(..., title="Type of Form (ccf/ddi)"),
):
    """
    Get a single Form based on the ID and the form type
    """
    if form_type == "ccf":
        cc_id = id
        results = get_cc(db, cc_id)
    elif form_type == "ddi":
        ddi_id = id
        results = get_ddi(db, ddi_id)
    else:
        return {"error": "Invalid form_type. Use 'ccd' or 'ddi'."}

    return results


@r.get("/{form_type}/img/{id}")
def get_cc_img_signed_url(
    id: int,
    db=Depends(get_db),
    s3_client=Depends(get_s3_client),
    form_type: str = Path(..., title="Type of Form (ccf/ddi)"),
):
    """
    Get the presigned URL for the image corresponding to a particular record
    """
    image_resource_exception = HTTPException(
        status_code=400, detail="Image storage location not defined"
    )
    if form_type == "ccf":
        ccid = id
        cc_db = get_cc(db, ccid)
        if cc_db.img_key is None:
            raise image_resource_exception
        if cc_db.aws_bucket is None:
            raise image_resource_exception
        url = create_presigned_url(s3_client, cc_db.aws_bucket, cc_db.img_key)
        return {"url": url}
    elif form_type == "ddi":
        ddi_id = id
        ddi_db = get_ddi(db, ddi_id)
        if ddi_db.img_key is None:
            raise image_resource_exception
        if ddi_db.aws_bucket is None:
            raise image_resource_exception
        url = create_presigned_url(s3_client, ddi_db.aws_bucket, ddi_db.img_key)
    else:
        return {"error": "Invalid form_type. Use 'ccd' or 'ddi'."}