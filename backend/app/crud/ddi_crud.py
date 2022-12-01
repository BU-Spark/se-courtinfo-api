from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic.types import UUID4
from app.schemas import ddi_schemas
import app.models.form_models as form_models
from starlette import status

def create_ddi(db: Session, ddi: ddi_schemas.DefendantDemoInfoCreate) -> form_models.DefendantDemoInfo:
    dd_ddi = form_models.DefendantDemoInfo(**ddi.dict())
    db.add(dd_ddi)
    db.commit()
    db.refresh(dd_ddi)
    return dd_ddi

def get_ddi(db: Session, ddi_id: UUID4) -> form_models.DefendantDemoInfo:
    ddi = db.query(form_models.DefendantDemoInfo).filter(form_models.DefendantDemoInfo.id == ddi_id).first()
    if not ddi:
        raise HTTPException(status_code=404, detail="ddi not found")
    return ddi

def update_ddi(db: Session, updater: str, ddi: ddi_schemas.DefendantDemoInfoCreate) -> form_models.DefendantDemoInfo:
    db_ddi = get_ddi(db, ddi.id)
    if not db_ddi:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Criminal Complaint form not found")
    update_data = ddi.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ddi, key, value)
    # Set updated by value
    db_ddi.updated_by = updater
    # Commit to DB
    db.add(db_ddi)
    db.commit()
    db.refresh(db_ddi)
    return db_ddi
