from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.schemas import ddi_schemas
import app.models.form_models as form_models

def create_ddi(db: Session, ddi: ddi_schemas.DefendantDemoInfoCreate) -> form_models.DefendantDemoInfo:
    dd_ddi = form_models.DefendantDemoInfo(**ddi.dict())
    db.add(dd_ddi)
    db.commit()
    db.refresh(dd_ddi)
    return dd_ddi
