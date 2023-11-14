from pydantic import BaseModel, UUID4
from typing import Optional
from uuid import UUID


class PhotoUploadBase(BaseModel):
    upload_id: Optional[UUID]
    photo_id: Optional[UUID]


class PhotoUploadCreate(PhotoUploadBase):
    upload_id: UUID
    photo_id: UUID


class PhotoUploadUpdate(PhotoUploadBase):
    pass


class PhotoUploadInDBBase(PhotoUploadBase):
    id: int

    class Config:
        orm_mode = True


class PhotoUpload(PhotoUploadInDBBase):
    pass


class PhotoUploadInDB(PhotoUploadInDBBase):
    pass
