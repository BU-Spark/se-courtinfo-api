from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.schemas import ddi_schemas
import app.models.form_models as form_models


def get_ddi(db: Session, ddi_id: int) -> form_models.DefendantDemoInfo:
    return db.query(form_models.DefendantDemoInfo).filter(
        form_models.DefendantDemoInfo.ddi_id == ddi_id).first()


def get_all_ddi(db: Session, skip: int = 0, limit: int = 100):
    return db.query(form_models.DefendantDemoInfo).order_by(form_models.DefendantDemoInfo.created_at.asc()).offset(
        skip).limit(limit).all()


def get_ddis(db: Session, skip: int = 0, limit: int = 250) -> List[form_models.DefendantDemoInfo]:
    return db.query(form_models.DefendantDemoInfo).offset(skip).limit(limit).all()


def create_ddi(db: Session, ddi: ddi_schemas.DefendantDemographicInfoCreate) -> form_models.DefendantDemoInfo:
    db_ddi = form_models.DefendantDemoInfo(**ddi.dict())
    db.add(db_ddi)
    db.commit()
    db.refresh(db_ddi)
    return db_ddi


def update_ddi(db: Session, updater: str, ddi: ddi_schemas.DefendantDemographicInfoUpdate) -> form_models.DefendantDemoInfo:
    db_ddi = get_ddi(db, ddi.ddi_id)
    if not db_ddi:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="DDI form not found")
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


def delete_ddi(db: Session, ddi_id: int):
    db_ddi = get_ddi(db, ddi_id)
    if not db_ddi:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Criminal Complaint form not found, did not delete")
    db.query(form_models.DefendantDemoInfo).filter(form_models.DefendantDemoInfo.ddi_id == ddi_id).delete()
    db.commit()