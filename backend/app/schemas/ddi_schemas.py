from enum import Enum
from typing import List, Optional, Tuple, TypedDict
from pydantic import UUID4, BaseModel, condecimal, conint

class PastMilitaryServiceDDI(TypedDict):
    branch_of_services: Optional[str]
    type_of_discharges: Optional[str]
    notes: Optional[str]

class EducationDDI(TypedDict):
    curr_student: Optional[bool]
    last_curr_school: Optional[str]
    last_grade: Optional[str]
    writes_eng: Optional[bool]
    reads_eng: Optional[bool]
    notes: Optional[str]

# Employment
class EmploymentDDI(TypedDict):
    verified_by: Optional[str]
    employed: Optional[bool]
    employer: Optional[str]
    phone: Optional[str]
    addr1: Optional[str]
    addr2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    emp_from: Optional[str]
    wages: Optional[int]
    period: Optional[str]
    notes: Optional[str]

# References
class ReferencesDDI(TypedDict):
    name: Optional[str]
    relationship: Optional[str]
    phone_number: Optional[str]
    note: Optional[str]

# Residence
class ResidenceDDI(TypedDict):
    verified_by: Optional[str]
    homeless: Optional[str]
    fixed_addr: Optional[int]
    phone_number: Optional[str]
    cell_phone: Optional[str]
    home_phone: Optional[str]
    email: Optional[str]
    lives_with: Optional[str]
    relationship: Optional[str]
    addr1: Optional[str]
    addr2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]
    len_at_pres_addr_years: Optional[int]
    len_at_pres_addr_months: Optional[int]
    len_at_pres_area_years: Optional[int]
    len_at_pres_area_months: Optional[int]
    len_at_pres_state_years: Optional[int]
    len_at_pres_state_months: Optional[int] 
    vehicle_access: Optional[int]
    public_trans_access: Optional[int]
    drivers_license: Optional[str]
    state_issued: Optional[str]

# Known Aliases
class KnownAliasesDDI(TypedDict):
    name: Optional[str]
    ssn: Optional[str]
    dob: Optional[str]

# Basic information
class BasicInfoDDI(TypedDict):
    case_number: Optional[str]
    name: Optional[str]
    ssn: Optional[str]
    sex: Optional[str]
    race: Optional[str]
    dob: Optional[str]
    age: Optional[int]
    birth_place: Optional[str]
    dep_living: Optional[int]
    primary_lang: Optional[str]
    marital_status: Optional[str]
    dep: Optional[int]
    sid_number: Optional[str]
    fbi_number: Optional[str]
    local_tracking: Optional[str]
    notes: Optional[str]

# For saving information from defendant demographic information form
class DefendantDemoInfoBase(BaseModel):
    basic: BasicInfoDDI
    known_aliases: KnownAliasesDDI
    residence: ResidenceDDI
    references: ReferencesDDI
    education: EducationDDI
    pass_military_services: PastMilitaryServiceDDI

class SexEnum(str, Enum):
    male = 'male'
    female = 'female'

class RaceEnum(str, Enum):
    white = 'white'
    black = 'black'
    asian = 'asian'
    other = 'other'
    unknown = 'unknown'

class RecommendationEnum(str, Enum):
    detain = 'detain'
    release_with = 'release with supervision'
    release_without = 'release without supervision'

class PrimaryChargeEnum(str, Enum):
    violent_felony_firearm = 'violent felony/firearm'
    violent_misdemeanor = 'violent misdemeanor'
    felony = 'non-violent felony'
    driving_under_influences = 'driving under the influence'
    misdemeanor = 'non-violent misdemeanor'
    fta_violent_felony_firearm = 'fta: violent felony/firearm'
    fta_violent_misdemeanor = 'fta: violent misdemeanor'
    fta_felony = 'fta: non-violent felony'
    fta_driving_under_influeces = 'fta: driving under the influences'
    fta_misdemeanor = 'fta: non-violent misdemeanor'

class DefendantDemoInfoBaseV1(BaseModel):
    zip: condecimal(max_digits=5, decimal_places=0)
    race: RaceEnum = 'other'
    sex: SexEnum = 'male'
    recommendation: Optional[RecommendationEnum]
    primary_charge_category: Optional[PrimaryChargeEnum]
    risk_level = conint(ge=1, le=6)
    rec_with_praxis: str
    dob: str
    charges: str

class DefendantDemoInfoCreate(DefendantDemoInfoBaseV1):
    created_by: UUID4
    img_key: str
    aws_bucket: str
    raw_text: str