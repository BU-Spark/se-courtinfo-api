import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base


class User(Base):
    """
    Represents a user in the database. This class corresponds to the 'users' table.
    Each field in the class is a column in the table, with various properties like
    uniqueness, indexing, and nullability.
    """
    __tablename__ = "users"

    # UUID field for the user's ID, generated automatically with 'gen_random_uuid()' function.
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"),
                index=True)

    # User's email address, must be unique.
    email = Column(String, unique=True, index=True, nullable=False)

    # User's first name.
    first_name = Column(String)

    # User's last name.
    last_name = Column(String)

    # Hashed password for the user, required for authentication.
    hashed_password = Column(String, nullable=False)

    # Boolean flag to indicate if the user's account is active.
    is_active = Column(Boolean, default=False)

    # Boolean flag to indicate if the user has superuser (admin) privileges.
    is_superuser = Column(Boolean, default=False)

    # Boolean flag to indicate if the user is authorized by the county.
    is_county_authorized = Column(Boolean, default=False)
