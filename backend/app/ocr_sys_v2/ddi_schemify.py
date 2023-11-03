'''
General Overview of the code in this file:
1. Gets the parsed text from the image (which has already been passed through the OCR API)
2. Passes the text into a function that fills in the appropriate fields for the ddi schema

The next step would be to validate the schema and then pass it into the database.
'''
import re
from typing import List, Optional
from array import array
import os
from PIL import Image
import sys
import time
from app.ocr_sys_v2.ocr_read import *
from app.schemas.cc_schemas import *
from app.schemas.user_schemas import *
from app.schemas.ddi_schemas import *


def ddi_schema_fill(text: str) -> DefendantDemographicInfoBase:
    '''
    A Defendant Demographic Info Form is made up of the following fields:
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
    This function takes in the text from the image and fills in the appropriate fields.
    '''
    first_name = text[first_name]
    last_name = text[last_name]
    date_of_birth = text[date_of_birth]
    zip_code = text[zip_code]
    charges = text[charges]
    race = text[race]
    sex = text[sex]
    recommendation = text[recommendation]
    primary_charge_category = text[primary_charge_category]
    risk_level = text[risk_level]
    praxis = text[praxis]
    return DefendantDemographicInfoBase(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, 
                                        zip_code=zip_code, charges=charges, race=race, sex=sex, 
                                        recommendation=recommendation, primary_charge_category=primary_charge_category,
                                        risk_level=risk_level, praxis=praxis)

#TESTS (THIS IS ASSUMING THAT OCR PROCESSING HAS ALREADY BEEN DONE CORRECTLY)