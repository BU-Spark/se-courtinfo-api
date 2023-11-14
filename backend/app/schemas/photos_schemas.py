from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional


class PhotoBase(BaseModel):
    Image: Optional[bytes]


class PhotoCreate(PhotoBase):
    created_by: UUID4


class Photo(PhotoBase):
    id: int
    created_at: datetime
    created_by: UUID4


class PhotoUpdate(PhotoBase):
    id: int
    updated_by: UUID4


class PhotoFull(PhotoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: UUID4
    updated_by: Optional[UUID4]
