from sqlalchemy.dialects.postgresql import UUID
from app.db.session import utcnow
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Date, Table
from sqlalchemy.orm import relationship, declared_attr


class HasPhotos:
    """
    A mixin to provide a relationship to a 'photos' table. This creates a new 
    'photos_association' table for each parent model that uses this mixin, 
    allowing the parent to be associated with multiple photos.
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
        return relationship("Photo", secondary=photo_association)


class HasCreatedAtUpdatedAt:
    """
    A mixin to add common fields 'createdAt', 'updatedAt', 'createdBy', and 'updatedBy' to a model.
    These fields are useful for tracking when a record was created or last updated and by whom.
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
    Represents a criminal complaint record in the database. Each field in this class
    corresponds to a column in the 'criminal_complaints' table.
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
    Represents defendant demographic information in the database. Each field in this class
    corresponds to a column in the 'defendant_demographic_info' table.
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
    Represents different types of forms in the database. Each field in this class
    corresponds to a column in the 'form_types' table. It links to criminal complaints
    and defendant demographic info.
    """
    __tablename__ = "form_types"

    id = Column(Integer, primary_key=True, index=True)
    cc_id = Column(Integer, ForeignKey('criminal_complaints.cc_id'))
    ddi_id = Column(Integer, ForeignKey('defendant_demographic_info.ddi_id'))

    form_type_description = Column(String)
    table_name = Column(String)

# ... (Continue with the rest of the classes)
