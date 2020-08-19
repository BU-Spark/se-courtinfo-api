from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CriminalComplaintBase(BaseModel):
    docket: Optional[str]
    number_of_counts: Optional[int]
    defen_name_adr: Optional[str]
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


class CriminalComplaintCreate(CriminalComplaintBase):
    #created_by: str
    #created_at: datetime

    class Config:
        orm_mode = True


class CriminalComplaintUpdate(CriminalComplaintBase):
    cc_id: int
    updated_by: str

    class Config:
        orm_mode = True


class CriminalComplaintInDBBase(CriminalComplaintBase):
    cc_id: int
    created_by: str
    updated_by: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CriminalComplaint(CriminalComplaintInDBBase):
    pass
