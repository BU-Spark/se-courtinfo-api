from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class FormTypeBase(BaseModel):
    name: UUID4
    form_type_description: Optional[str]
    table_name: Optional[str]


class FormTypeCreateEmpty(FormTypeBase):
    pass


class FormTypeCreate(FormTypeBase):
    form_type_description: str
    table_name: str


class FormType(FormTypeBase):
    id: int


class FormTypeUpdate(FormTypeBase):
    id: int


class FormTypeWithAudit(FormTypeBase):
    created_by: Optional[UUID4]
    updated_by: Optional[UUID4]


class FormTypeCreateWithAudit(FormTypeWithAudit):
    form_type_description: str
    table_name: str


class FormTypeFull(FormTypeWithAudit):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class FormTypeUpdateWithAudit(FormTypeFull):
    pass
