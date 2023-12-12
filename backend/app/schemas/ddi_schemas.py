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
from pydantic import BaseModel, constr, conint, validator, Literal
from datetime import datetime, date
from typing import Optional
from uuid import UUID4
# Assuming this import is needed for other parts of your code
from schemas.user_schemas import User


def normalize_string(string: str) -> str:
    """
    Function to normalize a string by stripping leading and trailing whitespace
    and converting it to lowercase.
    :param string: Input string to be normalized
    :return: Normalized string
    """
    return string.strip().lower()


# Custom string type with normalization applied
str_normalized = constr(strip_whitespace=True, to_lower=True)


class DefendantDemographicInfoBase(BaseModel):
    """
    Base Pydantic model for defendant demographic information. Includes fields
    to capture various attributes of a defendant.
    """
    first_name: str_normalized  # Defendant's first name, normalized
    last_name: str_normalized  # Defendant's last name, normalized
    date_of_birth: date  # Defendant's date of birth
    # Defendant's ZIP code, normalized and validated
    zip_code: constr(strip_whitespace=True, to_lower=True,
                     min_length=5, max_length=5)
    charges: str_normalized  # Charges against the defendant, normalized
    race: Literal["white", "black", "asian",
                  "other", "unknown"]  # Defendant's race
    sex: Literal["male", "female"]  # Defendant's sex
    # Recommendation for defendant's handling
    recommendation: Literal["detain",
                            "release without supervision", "release without supervision"]
    primary_charge_category: str_normalized  # Primary charge category, normalized
    # Risk level, constrained integer between 1 and 6
    risk_level: conint(ge=1, le=6)
    praxis: Literal[
        "the recommendation is consistent with the praxis", "the recommendation is not consistent with the praxis"]  # Statement about the consistency of the recommendation with the praxis

    @validator("date_of_birth", pre=True)
    def parse_birthdate(cls, value: str):
        """
        Validator to parse the date of birth from a string.
        :param value: Date of birth string in the format 'mm/dd/yyyy'
        :return: Parsed date object
        """
        return datetime.strptime(value.strip(), "%m/%d/%Y").date()

    @validator("zip_code")
    def verify_zip_code(cls, value: str):
        """
        Validator to ensure the ZIP code is numeric.
        :param value: ZIP code string
        :return: ZIP code string if valid
        :raises ValueError: If ZIP code is not numeric
        """
        if not value.isdigit():
            raise ValueError("Zip code must be digits")
        return value

    _normalize_strings = validator('race', 'sex', 'recommendation', 'praxis', allow_reuse=True, pre=True)(
        normalize_string)

    class Config:
        orm_mode = True  # Allows the model to be compatible with ORM objects

# Additional models (DefendantDemographicInfoCreateEmpty, DefendantDemographicInfoCreate, etc.)
# follow a similar pattern, extending DefendantDemographicInfoBase and
# either making fields optional or adding additional fields like 'created_by', 'updated_by', etc.