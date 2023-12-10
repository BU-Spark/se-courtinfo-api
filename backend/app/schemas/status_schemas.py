from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID4
from datetime import datetime


class StatusBase(BaseModel):
    """
    Base Pydantic model for status. This class includes the fundamental fields
    that describe a status.
    """
    name: Optional[constr(strip_whitespace=True)
                   ]  # Name of the status, optional, with whitespace stripped
    description: Optional[str]  # Description of the status, optional


class StatusCreateEmpty(StatusBase):
    """
    Pydantic model for creating a new status without any additional fields.
    Inherits from StatusBase.
    """
    pass


class StatusCreate(StatusBase):
    """
    Pydantic model for creating a new status. Inherits from StatusBase,
    but can be extended with additional creation-specific fields if necessary.
    """
    pass


class Status(StatusBase):
    """
    Comprehensive Pydantic model for a status, including its unique identifier.
    Inherits from StatusBase.
    """
    id: int  # Unique identifier for the status


class StatusUpdate(StatusBase):
    """
    Pydantic model for updating an existing status. Inherits from StatusBase and
    includes the status's unique identifier for reference.
    """
    id: int  # Unique identifier for the status, necessary for updates


class StatusWithAudit(StatusBase):
    """
    Extended Pydantic model for a status with fields for audit information
    (who created and updated the status). Inherits from StatusBase.
    """
    created_by: Optional[UUID4]  # UUID of the user who created this status, optional
    # UUID of the user who last updated this status, optional
    updated_by: Optional[UUID4]


class StatusCreateWithAudit(StatusWithAudit):
    """
    Pydantic model for creating a new status with audit information.
    Inherits from StatusWithAudit.
    """
    pass


class StatusFull(StatusWithAudit):
    """
    Detailed Pydantic model for a status, including audit information and timestamps.
    Inherits from StatusWithAudit.
    """
    id: int  # Unique identifier for the status
    # Timestamp when the status was created, optional
    created_at: Optional[datetime]
    # Timestamp when the status was last updated, optional
    updated_at: Optional[datetime]


class StatusUpdateWithAudit(StatusFull):
    """
    Pydantic model for updating a status with audit information.
    Inherits from StatusFull and includes all the fields necessary for updating a status.
    """
    pass
