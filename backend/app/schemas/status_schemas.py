from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID4
from datetime import datetime

# The base class that includes common fields


class StatusBase(BaseModel):

    name: Optional[constr(strip_whitespace=True)]
    description: Optional[str]


class StatusCreateEmpty(StatusBase):
    pass


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int


class StatusUpdate(StatusBase):
    id: int


class StatusWithAudit(StatusBase):
    created_by: Optional[UUID4]
    updated_by: Optional[UUID4]


class StatusCreateWithAudit(StatusWithAudit):
    pass


class StatusFull(StatusWithAudit):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class StatusUpdateWithAudit(StatusFull):
    pass
