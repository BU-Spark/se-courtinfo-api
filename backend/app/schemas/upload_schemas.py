from datetime import datetime

from pydantic import BaseModel, UUID4, ByteSize


class FormTypeBase(BaseModel):
    name: str
    description: str
    # Name of table where the extracted data is stored
    table_name: str
    # Indicates length of form
    min_page_count: int
    # States if there might be a variable number of pages
    # for the same form type
    variable_page_count: bool

    class Config:
        orm_mode = True


class FormTypeCreate(FormTypeBase):
    created_by: UUID4
    updated_by: UUID4


class FormType(FormTypeBase):
    id: int
    created_by: UUID4
    updated_by: UUID4
    created_at: datetime
    updated_at: datetime


class PhotoBase(BaseModel):
    photo: ByteSize
    photo_number: int


class FormTypeBase(BaseModel):
    """
    Base Pydantic model for a form type. This class includes the fundamental fields
    that describe a form type.
    """
    name: str  # Name of the form type
    description: str  # Description of the form type
    table_name: str  # Name of the database table where the extracted data from this form type is stored
    min_page_count: int  # Minimum number of pages that this form type should have
    # Flag indicating if this form type can have a variable number of pages
    variable_page_count: bool

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class FormTypeCreate(FormTypeBase):
    """
    Pydantic model for creating a new form type. Inherits from FormTypeBase and adds
    fields for tracking the user who created and last updated the form type.
    """
    created_by: UUID4  # UUID of the user who created this form type
    updated_by: UUID4  # UUID of the user who last updated this form type


class FormType(FormTypeBase):
    """
    Comprehensive Pydantic model for a form type, including fields for tracking its creation and update.
    Inherits from FormTypeBase.
    """
    id: int  # Unique identifier for the form type
    created_by: UUID4  # UUID of the user who created this form type
    updated_by: UUID4  # UUID of the user who last updated this form type
    created_at: datetime  # Timestamp when the form type was created
    updated_at: datetime  # Timestamp when the form type was last updated


class PhotoBase(BaseModel):
    """
    Base Pydantic model for a photo. This class includes the basic fields that describe a photo.
    """
    photo: ByteSize  # Binary data of the photo
    # A number representing the photo (could be used for ordering or identification)
    photo_number: int

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class PhotoCreate(PhotoBase):
    """
    Pydantic model for creating a new photo. Inherits from PhotoBase and adds
    a field for tracking the user who created the photo.
    """
    created_by: UUID4  # UUID of the user who created this photo


class Photo(PhotoBase):
    """
    Comprehensive Pydantic model for a photo, including fields for tracking its creation.
    Inherits from PhotoBase.
    """
    id: int  # Unique identifier for the photo
    created_by: UUID4  # UUID of the user who created this photo
    created_at: datetime  # Timestamp when the photo was created

    class Config:
        orm_mode = True


class PhotoCreate(PhotoBase):
    created_by: UUID4


class Photo(PhotoBase):
    id: int
    created_by: UUID4
    created_at: datetime
