from pydantic import BaseModel, UUID4
from typing import Optional
from uuid import UUID


class PhotoUploadBase(BaseModel):
    """
    Base Pydantic model for a photo upload. This class includes the foundational fields
    that describe a photo upload association.
    """
    upload_id: Optional[UUID]  # UUID of the upload, optional
    photo_id: Optional[UUID]  # UUID of the photo, optional


class PhotoUploadCreate(PhotoUploadBase):
    """
    Pydantic model for creating a new photo upload association. Inherits from PhotoUploadBase
    and requires both upload_id and photo_id to be specified.
    """
    upload_id: UUID  # UUID of the upload, required for creation
    photo_id: UUID  # UUID of the photo, required for creation


class PhotoUploadUpdate(PhotoUploadBase):
    """
    Pydantic model for updating an existing photo upload association. Currently,
    it doesn't add any additional fields to the base model, but can be extended if needed.
    """
    pass


class PhotoUploadInDBBase(PhotoUploadBase):
    """
    Base Pydantic model representing a photo upload record in the database.
    Inherits from PhotoUploadBase and adds an 'id' field.
    """
    id: int  # Unique identifier for the photo upload association

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class PhotoUpload(PhotoUploadInDBBase):
    """
    Pydantic model representing a photo upload. Inherits from PhotoUploadInDBBase.
    Can be used for read operations where a simple representation is required.
    """
    pass


class PhotoUploadInDB(PhotoUploadInDBBase):
    """
    Detailed Pydantic model representing a photo upload record in the database.
    Inherits from PhotoUploadInDBBase. This model can be extended with additional
    fields specific to database records.
    """
    pass