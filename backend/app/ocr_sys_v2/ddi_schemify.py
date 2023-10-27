'''
General Overview of the code in this file:
1. Gets the parsed text from the image (which has already been passed through the OCR API)
2. Passes the text into a function that fills in the appropriate fields for the ddi schema

The next step would be to validate the schema and then pass it into the database.
'''

import re
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
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
    first_name = get_first_name(text)
    last_name = get_last_name(text)
    date_of_birth = get_date_of_birth(text)
    zip_code = get_zip_code(text)
    charges = get_charges(text)
    race = get_race(text)
    sex = get_sex(text)
    recommendation = get_recommendation(text)
    primary_charge_category = get_primary_charge_category(text)
    risk_level = get_risk_level(text)
    praxis = get_praxis(text)
    return
    #return DefendantDemographicInfoBase(first_name=first_name, ...)