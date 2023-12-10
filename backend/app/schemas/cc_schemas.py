from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4


class CriminalComplaintBase(BaseModel):
    """
    Base Pydantic model for a criminal complaint. This class includes optional fields
    that describe various aspects of a criminal complaint.
    """
    docket: Optional[str]  # Docket number of the complaint
    number_of_counts: Optional[int]  # Number of counts in the complaint
    defen_name: Optional[str]  # Defendant's name
    defen_adr: Optional[str]  # Defendant's address
    defen_DOB: Optional[str]  # Defendant's date of birth
    court_name_adr: Optional[str]  # Court name and address
    complaint_issued_date: Optional[str]  # Date the complaint was issued
    offense_date: Optional[str]  # Date of the offense
    arrest_date: Optional[str]  # Date of the arrest
    next_event_date: Optional[str]  # Date of the next event in the case
    next_event_type: Optional[str]  # Type of the next event
    next_event_room_session: Optional[str]  # Room or session of the next event
    offense_city: Optional[str]  # City where the offense occurred
    offense_adr: Optional[str]  # Address where the offense occurred
    police_dept: Optional[str]  # Police department involved
    police_incident_num: Optional[str]  # Police incident number
    OBTN: Optional[str]  # Officer's badge/identification number
    PCF_number: Optional[str]  # Police complaint form number
    defen_xref_id: Optional[str]  # Defendant's cross-reference ID
    offense_codes: Optional[str]  # Codes of the offenses
    raw_text: Optional[str]  # Raw text of the complaint


class CriminalComplaintCreate(CriminalComplaintBase):
    """
    Pydantic model for creating a new criminal complaint. Inherits from CriminalComplaintBase
    and adds fields for the creator's UUID, image key, AWS bucket, and raw text of the complaint.
    """
    created_by: UUID4  # UUID of the user who created this complaint
    img_key: str  # Image key for the complaint
    aws_bucket: str  # AWS bucket where the complaint image is stored
    raw_text: str  # Raw text of the complaint, required for creation

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class CriminalComplaintUpdate(CriminalComplaintBase):
    """
    Pydantic model for updating an existing criminal complaint. Inherits from CriminalComplaintBase
    and includes the complaint's unique identifier, updated_by UUID, and optional fields for image key, AWS bucket, and raw text.
    """
    cc_id: int  # Unique identifier for the criminal complaint, necessary for updates
    updated_by: UUID4  # UUID of the user who updated this complaint
    img_key: Optional[str]  # Image key for the complaint, optional for updates
    # AWS bucket where the complaint image is stored, optional for updates
    aws_bucket: Optional[str]
    raw_text: Optional[str]  # Raw text of the complaint, optional for updates

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class CriminalComplaintInDBBase(CriminalComplaintBase):
    """
    Base Pydantic model representing a criminal complaint record in the database.
    Inherits from CriminalComplaintBase and adds fields for complaint ID, audit information, and storage details.
    """
    cc_id: int  # Unique identifier for the criminal complaint
    created_by: UUID4  # UUID of the user who created this complaint
    # UUID of the user who updated this complaint, optional
    updated_by: Optional[UUID4]
    created_at: datetime  # Timestamp when the complaint was created
    # Timestamp when the complaint was last updated, optional
    updated_at: Optional[datetime]
    img_key: Optional[str]  # Image key for the complaint, optional
    # AWS bucket where the complaint image is stored, optional
    aws_bucket: Optional[str]
    raw_text: Optional[str]  # Raw text of the complaint, optional

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class CriminalComplaint(CriminalComplaintInDBBase):
    """
    Comprehensive Pydantic model for a criminal complaint, including full details.
    Inherits from CriminalComplaintInDBBase. Useful for detailed views.
    """
    pass


class CriminalComplaintOut(CriminalComplaintBase):
    """
    Pydantic model for outputting criminal complaint data. Inherits from CriminalComplaintBase
    and includes the complaint's unique identifier and key fields. This model is typically
    used when displaying complaint data in API responses or user interfaces.
    """
    cc_id: int  # Unique identifier for the criminal complaint
    docket: str  # Docket number of the complaint, required in output
    defen_name: str  # Defendant's name, required in output
    defen_adr: str  # Defendant's address, required in output

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects
