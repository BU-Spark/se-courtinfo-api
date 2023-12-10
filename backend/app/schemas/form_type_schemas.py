from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class FormTypeBase(BaseModel):
    """
    Base Pydantic model for a form type. This class includes essential fields that
    describe a form type.
    """
    name: UUID4  # UUID representing the name of the form type
    # Optional description of the form type
    form_type_description: Optional[str]
    # Optional name of the database table associated with this form type
    table_name: Optional[str]


class FormTypeCreateEmpty(FormTypeBase):
    """
    Pydantic model for creating a new form type with minimal fields.
    Inherits from FormTypeBase and does not add any additional fields.
    """
    pass


class FormTypeCreate(FormTypeBase):
    """
    Pydantic model for creating a new form type. Inherits from FormTypeBase and
    requires 'form_type_description' and 'table_name' fields to be specified.
    """
    form_type_description: str  # Description of the form type, required for creation
    table_name: str  # Name of the database table, required for creation


class FormType(FormTypeBase):
    """
    Comprehensive Pydantic model for a form type, including its unique identifier.
    Inherits from FormTypeBase.
    """
    id: int  # Unique identifier for the form type


class FormTypeUpdate(FormTypeBase):
    """
    Pydantic model for updating an existing form type. Inherits from FormTypeBase and
    includes the form type's unique identifier for reference.
    """
    id: int  # Unique identifier for the form type, necessary for updates


class FormTypeWithAudit(FormTypeBase):
    """
    Extended Pydantic model for a form type with fields for audit information
    (who created and updated the form type). Inherits from FormTypeBase.
    """
    created_by: Optional[UUID4]  # UUID of the user who created this form type, optional
    # UUID of the user who last updated this form type, optional
    updated_by: Optional[UUID4]


class FormTypeCreateWithAudit(FormTypeWithAudit):
    """
    Pydantic model for creating a new form type with audit information.
    Inherits from FormTypeWithAudit and requires 'form_type_description' and 'table_name'.
    """
    form_type_description: str  # Description of the form type, required for creation
    table_name: str  # Name of the database table, required for creation


class FormTypeFull(FormTypeWithAudit):
    """
    Detailed Pydantic model for a form type, including audit information and timestamps.
    Inherits from FormTypeWithAudit.
    """
    id: int  # Unique identifier for the
