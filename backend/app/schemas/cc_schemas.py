from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4


class CriminalComplaintBase(BaseModel):
    docket: Optional[str]
    number_of_counts: Optional[int]
    defen_name: Optional[str]
    defen_adr: Optional[str]
    defen_DOB: Optional[str]
    court_name_adr: Optional[str]
    complaint_issued_date: Optional[str]
    offense_date: Optional[str]
    arrest_date: Optional[str]
    next_event_date: Optional[str]
    next_event_type: Optional[str]
    next_event_room_session: Optional[str]
    offense_city: Optional[str]
    offense_adr: Optional[str]
    police_dept: Optional[str]
    police_incident_num: Optional[str]
    OBTN: Optional[str]
    PCF_number: Optional[str]
    defen_xref_id: Optional[str]
    offense_codes: Optional[str]
    raw_text: Optional[str]


class CriminalComplaintCreate(CriminalComplaintBase):
    created_by: UUID4
    img_key: str
    aws_bucket: str
    raw_text: str

    class Config:
        orm_mode = True


class CriminalComplaintUpdate(CriminalComplaintBase):
    cc_id: int
    updated_by: UUID4
    img_key: Optional[str]
    aws_bucket: Optional[str]
    raw_text: Optional[str]

    class Config:
        orm_mode = True


class CriminalComplaintInDBBase(CriminalComplaintBase):
    cc_id: int
    created_by: UUID4
    updated_by: Optional[UUID4]
    created_at: datetime
    updated_at: Optional[datetime]
    img_key: Optional[str]
    aws_bucket: Optional[str]
    raw_text: Optional[str]

    class Config:
        orm_mode = True


class CriminalComplaint(CriminalComplaintInDBBase):
    pass


class CriminalComplaintOut(CriminalComplaintBase):
    cc_id: int
    docket: str
    defen_name: str
    defen_adr: str

    class Config:
        orm_mode = True
