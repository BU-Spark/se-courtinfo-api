from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional


class PhotoBase(BaseModel):
    """
    Base Pydantic model for a photo. This class includes the basic field that describes a photo.
    """
    Image: Optional[bytes]  # Binary data of the photo, optional


class PhotoCreate(PhotoBase):
    """
    Pydantic model for creating a new photo. Inherits from PhotoBase and adds
    a field for the UUID of the user who created the photo.
    """
    created_by: UUID4  # UUID of the user who created this photo


class Photo(PhotoBase):
    """
    Comprehensive Pydantic model for a photo, including its unique identifier and
    creation details. Inherits from PhotoBase.
    """
    id: int  # Unique identifier for the photo
    created_at: datetime  # Timestamp when the photo was created
    created_by: UUID4  # UUID of the user who created this photo


class PhotoUpdate(PhotoBase):
    """
    Pydantic model for updating an existing photo. Inherits from PhotoBase and
    includes fields for the photo's unique identifier and the UUID of the user updating the photo.
    """
    id: int  # Unique identifier for the photo, necessary for updates
    updated_by: UUID4  # UUID of the user who is updating this photo


class PhotoFull(PhotoBase):
    """
    Detailed Pydantic model for a photo, including full audit information like creation and
    last update details. Inherits from PhotoBase.
    """
    id: int  # Unique identifier for the photo
    created_at: datetime  # Timestamp when the photo was created
    # Timestamp when the photo was last updated, optional
    updated_at: Optional[datetime]
    created_by: UUID4  # UUID of the user who created this photo
    # UUID of the user who last updated this photo, optional
    updated_by: Optional[UUID4]
