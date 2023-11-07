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
import sys
import json

# from app.ocr_sys_v2.ocr_read import *
# from app.schemas.user_schemas import *
# from app.schemas.ddi_schemas import *
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
    
def get_dob(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the date of birth.
    '''
    dob = re.search(r'DOB:\s*(.+)', text)
    if dob:
        return dob.group(1)
    else:
        return None

def get_ssn(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the social security number.
    '''
    ssn = re.search(r'SSN:\s*(.+)', text)
    if ssn:
        return ssn.group(1)
    else:
        return None
    
def get_sex(text: str) -> Optional[str]:
    sex = re.search(r'Sex:\s*(.+)', text)
    if sex:
        return sex.group(1).split(' ')[0][0]
    else:
        return None

def get_race(text: str) -> Optional[str]:
    race = re.search(r'Race:\s*(.+)', text)
    if race:
        return race.group(1)
    else:
        None
    
def get_age(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the age.
    '''
    age = re.search(r'Age:\s*(.+)', text)
    if age:
        return age.group(1).split(' ')[0]
    else:
        return None
      

def ddi_schema_fill(text: str):
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
    page1 = text['pages'][0]['lines']
    #page2 = text['pages'][1]['lines']
    first_name = get_first_name(page1[4]['content'])
    last_name = get_last_name(page1[4]['content'])
    date_of_birth = get_dob(page1[5]['content'])
    ssn = get_ssn(page1[6]['content'])
    sex = get_sex(page1[7]['content'])
    race = get_race(page1[7]['content'])
    age = get_age(page1[8]['content'])
    

    print(first_name)
    print(last_name)
    print(date_of_birth)
    print(ssn)
    print(sex)
    print(race)
    print(age)
    # return DefendantDemographicInfoBase(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, ssn = ssn
    #                                     zip_code=zip_code, charges=charges, race=race, sex=sex, 
    #                                     recommendation=recommendation, primary_charge_category=primary_charge_category,
    #                                     risk_level=risk_level, praxis=praxis)
    return text
#TESTS (THIS IS ASSUMING THAT OCR PROCESSING HAS ALREADY BEEN DONE CORRECTLY)

with open('backend/app/ocr_sys_v2/test_output.json') as json_file:
        text = json.load(json_file)

ddi_schema_fill(text)