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

    class Config:
        orm_mode = True


class PhotoCreate(PhotoBase):
    created_by: UUID4


class Photo(PhotoBase):
    id: int
    created_by: UUID4
    created_at: datetime
