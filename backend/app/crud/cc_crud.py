from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.schemas import cc_schemas
from app.models import cc_models


def get_cc(db: Session, cc_id: int) -> cc_models.CriminalComplaint:
    return db.query(cc_models.CriminalComplaint).filter(
        cc_models.CriminalComplaint.cc_id == cc_id).first()


def get_cc_by_ident(db: Session, date_of_birth: str, def_name_adr: str) -> cc_models.CriminalComplaint:
    return db.query(cc_models.CriminalComplaint).filter(
        cc_models.CriminalComplaint.defen_DOB == date_of_birth and
        cc_models.CriminalComplaint.defen_name_adr.like(def_name_adr)
    )


def get_criminal_complaints(db: Session, skip: int = 0, limit: int = 250):
    return db.query(cc_models.CriminalComplaint).offset(skip).limit(limit).all()


def create_cc(db: Session, cc: cc_schemas.CriminalComplaintCreate) -> cc_models.CriminalComplaint:
    db_cc = cc_models.CriminalComplaint(**cc.dict())
    db.add(db_cc)
    db.commit()
    db.refresh(db_cc)
    return db_cc


def update_cc(db: Session, updater: str, cc: cc_schemas.CriminalComplaintUpdate) -> cc_models.CriminalComplaint:
    db_cc = get_cc(db, cc.cc_id)
    if not db_cc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Criminal Complaint form not found")
    update_data = cc.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cc, key, value)
    # Set updated by value
    db_cc.updated_by = updater
    # Commit to DB
    db.add(db_cc)
    db.commit()
    db.refresh(db_cc)
    return db_cc


def delete_cc(db: Session, cc_id: int):
    db_cc = get_cc(db, cc_id)
    if not db_cc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Criminal Complaint form not found, did not delete")
    db.query(cc_models.CriminalComplaint).filter(cc_models.CriminalComplaint.cc_id == cc_id).delete()
    db.commit()
