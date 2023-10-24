from datetime import datetime, date
from enum import Enum
from typing import Optional, Literal
from typing_extensions import TypedDict
from pydantic import UUID4, BaseModel, condecimal, conint, validator, constr

# class PastMilitaryServiceDDI(TypedDict):
#     branch_of_services: Optional[str]
#     type_of_discharges: Optional[str]
#     notes: Optional[str]
#
# class EducationDDI(TypedDict):
#     curr_student: Optional[bool]
#     last_curr_school: Optional[str]
#     last_grade: Optional[str]
#     writes_eng: Optional[bool]
#     reads_eng: Optional[bool]
#     notes: Optional[str]
#
# # Employment
# class EmploymentDDI(TypedDict):
#     verified_by: Optional[str]
#     employed: Optional[bool]
#     employer: Optional[str]
#     phone: Optional[str]
#     addr1: Optional[str]
#     addr2: Optional[str]
#     city: Optional[str]
#     state: Optional[str]
#     zip: Optional[str]
#     emp_from: Optional[str]
#     wages: Optional[int]
#     period: Optional[str]
#     notes: Optional[str]
#
# # References
# class ReferencesDDI(TypedDict):
#     name: Optional[str]
#     relationship: Optional[str]
#     phone_number: Optional[str]
#     note: Optional[str]
#
# # Residence
# class ResidenceDDI(TypedDict):
#     verified_by: Optional[str]
#     homeless: Optional[str]
#     fixed_addr: Optional[int]
#     phone_number: Optional[str]
#     cell_phone: Optional[str]
#     home_phone: Optional[str]
#     email: Optional[str]
#     lives_with: Optional[str]
#     relationship: Optional[str]
#     addr1: Optional[str]
#     addr2: Optional[str]
#     city: Optional[str]
#     state: Optional[str]
#     zip: Optional[int]
#     len_at_pres_addr_years: Optional[int]
#     len_at_pres_addr_months: Optional[int]
#     len_at_pres_area_years: Optional[int]
#     len_at_pres_area_months: Optional[int]
#     len_at_pres_state_years: Optional[int]
#     len_at_pres_state_months: Optional[int]
#     vehicle_access: Optional[int]
#     public_trans_access: Optional[int]
#     drivers_license: Optional[str]
#     state_issued: Optional[str]
#
# # Known Aliases
# class KnownAliasesDDI(TypedDict):
#     name: Optional[str]
#     ssn: Optional[str]
#     dob: Optional[str]
#
# # Basic information
# class BasicInfoDDI(TypedDict):
#     case_number: Optional[str]
#     name: Optional[str]
#     ssn: Optional[str]
#     sex: Optional[str]
#     race: Optional[str]
#     dob: Optional[str]
#     age: Optional[int]
#     birth_place: Optional[str]
#     dep_living: Optional[int]
#     primary_lang: Optional[str]
#     marital_status: Optional[str]
#     dep: Optional[int]
#     sid_number: Optional[str]
#     fbi_number: Optional[str]
#     local_tracking: Optional[str]
#     notes: Optional[str]
#
# # For saving information from defendant demographic information form
# class DefendantDemoInfoBase(BaseModel):
#     basic: BasicInfoDDI
#     known_aliases: KnownAliasesDDI
#     residence: ResidenceDDI
#     references: ReferencesDDI
#     education: EducationDDI
#     pass_military_services: PastMilitaryServiceDDI
#
# class SexEnum(str, Enum):
#     male = 'male'
#     female = 'female'
#
# class RaceEnum(str, Enum):
#     white = 'white'
#     black = 'black'
#     asian = 'asian'
#     other = 'other'
#     unknown = 'unknown'
#
# class RecommendationEnum(str, Enum):
#     detain = 'detain'
#     release_with = 'release with supervision'
#     release_without = 'release without supervision'
#
# class PrimaryChargeEnum(str, Enum):
#     violent_felony_firearm = 'violent felony/firearm'
#     violent_misdemeanor = 'violent misdemeanor'
#     felony = 'non-violent felony'
#     driving_under_influences = 'driving under the influence'
#     misdemeanor = 'non-violent misdemeanor'
#     fta_violent_felony_firearm = 'fta: violent felony/firearm'
#     fta_violent_misdemeanor = 'fta: violent misdemeanor'
#     fta_felony = 'fta: non-violent felony'
#     fta_driving_under_influeces = 'fta: driving under the influences'
#     fta_misdemeanor = 'fta: non-violent misdemeanor'
#
# class DefendantDemoInfoBaseV1(BaseModel):
#     zip: condecimal(max_digits=5, decimal_places=0)
#     race: RaceEnum = 'other'
#     sex: SexEnum = 'male'
#     recommendation: Optional[RecommendationEnum]
#     primary_charge_category: Optional[PrimaryChargeEnum]
#     risk_level = conint(ge=1, le=6)
#     rec_with_praxis: str
#     dob: str
#     charges: str
#
# class DefendantDemoInfoCreate(DefendantDemoInfoBaseV1):
#     created_by: UUID4
#     img_key: str
#     aws_bucket: str
#     raw_text: str
#
# class DefendantDemographicInfoBase(BaseModel):
#     zip: condecimal(max_digits=5, decimal_places=0)
#     race: Literal["white"]
#
#     @validator('*', pre=True)
#     def lower_case(cls, v):
#         if isinstance(v, str):
#             return v.split('|')
#         return v
from schemas.user_schemas import User


def normalize_string(string: str) -> str:
    """
    A function to strip leading and trailing whitespace
    and lower case the input string
    :param string: Input string
    :type string: str
    :return: normalized string
    :rtype: str
    """
    return string.strip().lower()


str_normalized = constr(strip_whitespace=True, to_lower=True)


class DefendantDemographicInfoBase(BaseModel):
    first_name: str_normalized
    last_name: str_normalized
    date_of_birth: date
    zip_code: constr(strip_whitespace=True, to_lower=True, min_length=5, max_length=5)
    charges: str_normalized
    race: Literal["white", "black", "asian", "other", "unknown"]
    sex: Literal["male", "female"]
    recommendation: Literal["detain", "release without supervision", "release without supervision"]
    primary_charge_category: str_normalized
    risk_level: conint(ge=1, le=6)
    praxis: Literal[
        "the recommendation is consistent with the praxis", "the recommendation is not consistent with the praxis"]

    @validator("date_of_birth", pre=True)
    def parse_birthdate(cls, value: str):
        return datetime.strptime(
            value.strip(),
            "%m/%d/%Y"
        ).date()

    @validator("zip_code")
    def verify_zip_code(cls, value: str):
        if not value.isdigit():
            raise ValueError("Zip code must be digits")

    _normalize_strings = validator('race', 'sex', 'recommendation', 'praxis', allow_reuse=True, pre=True)(
        normalize_string)

    class Config:
        orm_mode = True


class DefendantDemographicInfoCreateEmpty(DefendantDemographicInfoBase):
    first_name: Optional[str_normalized]
    last_name: Optional[str_normalized]
    date_of_birth: Optional[date]
    zip_code: Optional[constr(strip_whitespace=True, to_lower=True, min_length=5, max_length=5)]
    charges: Optional[str_normalized]
    race: Optional[Literal["white", "black", "asian", "other", "unknown"]]
    sex: Optional[Literal["male", "female"]]
    recommendation: Optional[Literal["detain", "release without supervision", "release without supervision"]]
    primary_charge_category: Optional[str_normalized]
    risk_level: Optional[conint(ge=1, le=6)]
    praxis: Optional[Literal[
        "the recommendation is consistent with the praxis", "the recommendation is not consistent with the praxis"]]
    created_by: UUID4
    updated_by: UUID4


class DefendantDemographicInfoCreate(DefendantDemographicInfoBase):
    created_by: UUID4
    updated_by: UUID4


class DefendantDemographicInfo(DefendantDemographicInfoBase):
    id: int

    created_by: UUID4
    updated_by: UUID4
    updated_at: datetime
    created_at: datetime


class DefendantDemographicInfoUpdate(DefendantDemographicInfoBase):
    id: int
    updated_by: UUID4
