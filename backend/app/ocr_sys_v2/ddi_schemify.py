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

def get_first_name(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the first name.
    '''
    name = re.search(r'Name:\s*(.+)', text)
    first_name = name.group(1).split(' ')[0]
    if name:
        return first_name
    else:
        return None

def get_last_name(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the last name.
    '''
    name = re.search(r'Name:\s*(.+)', text)
    last_name = name.group(1).split(' ')[1]
    if name:
        return last_name
    else:
        return None

def get_date_of_birth(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the date of birth.
    '''
    dob = re.search(r'DOB:\s*(.+)', text)
    if dob:
        return dob.group(1)
    else:
        return None

def get_zip_code(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the zip code.
    '''
    zip_code = re.search(r'Zip:\s*(.+)', text)
    if zip_code:
        return zip_code.group(1)
    else:
        return None

def get_charges(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the charges.
    '''
    charges = re.search(r'Charges:\s*(.+)', text)
    if charges:
        return charges.group(1)
    else:
        return None

def get_race(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the race.
    '''
    race = re.search(r'Race:\s*(.+)', text)
    if race:
        return race.group(1)
    else:
        return None

def get_sex(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the sex of the user.
    '''
    sex = re.search(r'Sex:\s*(.+)', text)
    if sex:
        return sex.group(1)
    else:
        return None
    
def get_recommendation(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the recommendation.
    '''
    recommendation = re.search(r'Recommendation:\s*(.+)', text)
    if recommendation:
        return recommendation.group(1)
    else:
        return None

def get_primary_charge_category(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the primary charge category.
    '''
    primary_charge_category = re.search(r'Primary Charge Category:\s*(.+)', text)
    if primary_charge_category:
        return primary_charge_category.group(1)
    else:
        return None

def get_risk_level(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the risk level.
    '''
    risk_level = re.search(r'Risk Level:\s*(.+)', text)
    if risk_level:
        return risk_level.group(1)
    else:
        return None

def get_praxis(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the praxis.
    '''
    praxis = re.search(r'Praxis:\s*(.+)', text)
    if praxis:
        return praxis.group(1)
    else:
        return None

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
    return DefendantDemographicInfoBase(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, 
                                        zip_code=zip_code, charges=charges, race=race, sex=sex, 
                                        recommendation=recommendation, primary_charge_category=primary_charge_category,
                                        risk_level=risk_level, praxis=praxis)

#TESTS (THIS IS ASSUMING THAT OCR PROCESSING HAS ALREADY BEEN DONE CORRECTLY)
print(get_first_name("Name: John Doe"), get_last_name("Name: John Doe"))
print(get_date_of_birth("DOB: 01/01/2000"))
print(get_zip_code("Zip: 12345"))
print(get_charges("Charges: 12345"))
print(get_sex("Sex: M"))
print(get_race("Race: White"))
