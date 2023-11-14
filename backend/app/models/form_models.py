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

    created_at = Column(DateTime(timezone=True),
                        server_default=utcnow(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow(),
                        server_default=utcnow(), nullable=False)


class CriminalComplaint(HasCreatedAtUpdatedAt, Base):
    """
    This represents how CC are stored in the database, each field is a column with certain properties etc.
    When a record is retrived from the database it will be of this type.
    """
    __tablename__ = "criminal_complaints"

    cc_id = Column(Integer, primary_key=True, index=True)
    docket = Column(String)
    defen_name = Column(String)
    defen_adress = Column(String)
    defen_date_of_birth = Column(Date)
    complaint_issued_date = Column(Date)
    offense_date = Column(Date)
    arrest_date = Column(Date)
    court_name_adress = Column(String)
    police_incident_number = Column(String)
    ofense_codes = Column(String)


class DefendantDemoInfo(Base):
    """
    This represents how DDI are stored in the database, each field is a column with certain properties etc.
    When a record is retrived from the database it will be of this type.
    """
    __tablename__ = "defendant_demographic_info"
    ddi_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    zip_code = Column(String)
    charges = Column(String)
    race = Column(String)
    sex = Column(String)
    recommendation = Column(String)
    primary_charge_category = Column(String)
    risk_level = Column(String)
    praxis = Column(String)


class FormType(Base):
    """
    This represents how FormTypes are stored in the database, each field is a column with certain properties etc.
    When a record is retrived from the database it will be of this type.
    """
    __tablename__ = "form_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(UUID(as_uuid=True), ForeignKey('cc.id, ddi.id'))
    form_type_description = Column(String)
    table_name = Column(String)


class Upload(Base):

    __table__ = "upload"

    id = Column(Integer, primary_key=True, index=True)
    form_type = Column(UUID(as_uuid=True), ForeignKey('form_type_id.id'))
    form_id = Column(Integer)
    status = Column(UUID(as_uuid=True), ForeignKey('status.id'))


class Photo(Base):
    id = Column(Integer, primary_key=True, index=True)
    Image = Column(LargeBinary)
    created_at = Column(DateTime(timezone=True), server_default=utcnow())
    updated_at = Column(DateTime(timezone=True), onupdate=utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))


class PhotoUpload(Base):
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(UUID(as_uuid=True), ForeignKey('upload.id'))
    photo_id = Column(UUID(as_uuid=True), ForeignKey('photo.id'))


class OCRResultMetaData(Base):
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(UUID(as_uuid=True), ForeignKey('upload.id'))
    field_name = Column(String)
    ocr_result = Column(Integer)


class Status(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
