from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic.types import UUID4
from app.schemas import ddi_schemas
import app.models.form_models as form_models

def create_ddi(db: Session, ddi: ddi_schemas.DefendantDemoInfoCreate) -> form_models.DefendantDemoInfo:
    dd_ddi = form_models.DefendantDemoInfo(**ddi.dict())
    db.add(dd_ddi)
    db.commit()
    db.refresh(dd_ddi)
    return dd_ddi

def get_ddi(db: Session, ddi_id: UUID4) -> ddi_schemas.DefendantDemoInfoBaseV1:
    ddi = db.query(form_models.DefendantDemoInfo).filter(form_models.DefendantDemoInfo.id == ddi_id).first()
    if not ddi:
        raise HTTPException(status_code=404, detail="ddi not found")
    return ddi
