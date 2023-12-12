from pydantic import BaseModel, UUID4
import typing as t


class UserBase(BaseModel):
    """
    Base Pydantic model for a user. This class serves as the foundational model
    from which other user-related models will inherit. It includes basic user fields.
    """
    email: str  # User's email address
    is_active: bool = False  # Flag indicating if the user's account is active
    # Flag indicating if the user has superuser (admin) privileges
    is_superuser: bool = False
    # Flag indicating if the user is authorized by the county
    is_county_authorized: bool = False
    first_name: str = None  # User's first name
    last_name: str = None  # User's last name


class UserOut(UserBase):
    """
    Pydantic model for user output. Inherits from UserBase and adds an 'id' field,
    which is useful for operations where user identity needs to be confirmed, like in responses.
    """
    id: UUID4  # Unique identifier for the user


class UserCreate(UserBase):
    """
    Pydantic model for creating a new user. Inherits from UserBase and adds a
    'password' field, required for creating a new user account.
    """
    password: str  # User's password

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class UserEdit(UserBase):
    """
    Pydantic model for editing an existing user. Inherits from UserBase and
    adds an optional 'password' field for scenarios where the password might be updated.
    """
    password: t.Optional[str] = None  # User's password (optional for edits)

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class User(UserBase):
    """
    Comprehensive Pydantic model for a user, including the user's unique identifier.
    Inherits from UserBase and is typically used for detailed user views.
    """
    id: UUID4  # Unique identifier for the user

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects


class Token(BaseModel):
    """
    Pydantic model representing an authentication token.
    """
    access_token: str  # The token string
    token_type: str  # Type of the token (e.g., bearer)


class TokenData(BaseModel):
    """
    Pydantic model for the payload data within an authentication token.
    """
    email: str = None  # Email address associated with the token
    # Permissions or role associated with the token (default is 'user')
    permissions: str = "user"