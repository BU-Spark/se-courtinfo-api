from sqlalchemy.dialects.postgresql import UUID

from app.db.session import utcnow
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Date, Table
from sqlalchemy.orm import relationship, declared_attr


class HasPhotos:
    """HasPhotos mixin, creates a new photos_association
    table for each parent.

    """

    @declared_attr
    def photos(cls):
        photo_association = Table(
            "%s_photos" % cls.__tablename__,
            cls.metadata,
            Column("photo_id", ForeignKey("photo.id"), primary_key=True),
            Column(
                "%s_id" % cls.__tablename__,
                ForeignKey("%s.id" % cls.__tablename__),
                primary_key=True,
            ),
        )
        return relationship(Photo, secondary=photo_association)


class HasCreatedAtUpdatedAt:
    """
    HasCreatedAtUpdatedAt add createdAt, updatedAt and createdBy and updatedBy fields
    to the inheritted class
    """

    @declared_attr
    def created_by(self):
        return Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    @declared_attr
    def updated_by(self):
        return Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow(), server_default=utcnow(), nullable=False)


class CriminalComplaint(HasCreatedAtUpdatedAt, Base):
    """
    This represents how CC are stored in the database, each field is a column with certain properties etc.
    When a record is retrived from the database it will be of this type.
    """
    __tablename__ = "criminal_complaints"

    cc_id = Column(Integer, primary_key=True, index=True)
    docket = Column(String)
    number_of_counts = Column(Integer)
    defen_name = Column(String)
    defen_adr = Column(String)
    defen_DOB = Column(String)
    court_name_adr = Column(String)
    complaint_issued_date = Column(String)
    offense_date = Column(String)
    arrest_date = Column(String)
    next_event_date = Column(String)
    next_event_type = Column(String)
    next_event_room_session = Column(String)
    offense_city = Column(String)
    offense_adr = Column(String)
    offense_codes = Column(String)
    police_dept = Column(String)
    police_incident_num = Column(String)
    OBTN = Column(String)
    PCF_number = Column(String)
    defen_xref_id = Column(String)
    raw_text = Column(String)
    img_key = Column(String)
    aws_bucket = Column(String)


class DefendantDemographicInfo(HasPhotos, HasCreatedAtUpdatedAt, Base):
    """"
    Everything is marked optional because validation is handled by pydantic.
    """
    __tablename__ = 'defendant_demographic_info'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    zip_code = Column(String, nullable=True)
    charges = Column(String, nullable=True)
    race = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)
    primary_charge_category = Column(String, nullable=True)
    risk_level = Column(String, nullable=True)
    praxis = Column(String, nullable=True)
    photos = relationship("Photo", back_populates="parent")


class Photo(Base, HasCreatedAtUpdatedAt):
    __table__ = "photo"
    id = Column(Integer, primary_key=True, index=True)
    photo = Column(LargeBinary)
    photo_number = Column(Integer)


class FormType(Base, HasCreatedAtUpdatedAt):
    __table__ = "form_type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    table_name = Column(String)
    min_page_count = Column(Integer)
    variable_page_count = Column(bool)
