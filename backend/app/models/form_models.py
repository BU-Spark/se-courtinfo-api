from sqlalchemy.dialects.postgresql import UUID

from app.db.session import utcnow
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey



class CriminalComplaint(Base):
    """
    This represents how CC are stored in the database, each field is a column with certain properties etc.
    When a record is retrived from the database it will be of this type.
    """
    __tablename__ = "criminal_complaints"

    cc_id = Column(Integer, primary_key=True, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime(timezone=True), server_default=utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow())
    docket = Column(String)
    number_of_counts = Column(Integer)
    defen_name = Column(String)
    defen_adr = Column(String)
    defen_DOB = Column(String)
    court_name_adr = Column(String)
    complaint_issued_date = Column(String)
    offense_date = Column(String)
    arrest_date = Column(String)
    next_event_date = Column(String)
    next_event_type = Column(String)
    next_event_room_session = Column(String)
    offense_city = Column(String)
    offense_adr = Column(String)
    offense_codes = Column(String)
    police_dept = Column(String)
    police_incident_num = Column(String)
    OBTN = Column(String)
    PCF_number = Column(String)
    defen_xref_id = Column(String)
    raw_text = Column(String)
    img_key = Column(String)
    aws_bucket = Column(String)
