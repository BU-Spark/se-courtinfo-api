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
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.ocr_sys_v2.ocr_read import *
from app.schemas.user_schemas import *
from app.schemas.ddi_schemas import *
      
# DATABASE_URL = "???"  # Update with your actual database URL

# engine = create_engine(DATABASE_URL)
# SessionLocal = Session(bind=engine)


def ddi_schema_fill() -> Optional[DefendantDemographicInfoBase]:
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
    with open('backend/app/ocr_sys_v2/test_output.json') as json_file:
        text = json.load(json_file)

    fields = text['documents'][0]['fields']

    first_name = fields['Name']['value'].split(' ')[0]
    last_name = fields['Name']['value'].split(' ')[1]
    date_of_birth = fields['DOB']['value']
    zip_code = fields['Zip']['value']
    charges = fields['Charge']['value']
    race = fields['Race']['value']
    sex = fields['Sex']['value']
    recommendation = fields['Recommendation']['value']
    primary_charge_category = fields['PrimaryCharge']['value']
    risk_level = fields['RiskLevel']['value']
    praxis = fields['Praxis']['value']
    
    print(first_name, last_name, date_of_birth, zip_code, charges, race, sex, recommendation, primary_charge_category, risk_level, praxis)
    if not (first_name and last_name and date_of_birth and zip_code and charges and race and sex 
        and recommendation and primary_charge_category and risk_level and praxis):
        return False
    else:
        #add to database?
        # dummy method
        schema = DefendantDemographicInfo(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
                                            zip_code=zip_code, charges=charges, race=race, sex=sex, 
                                            recommendation=recommendation, primary_charge_category=primary_charge_category,
                                            risk_level=risk_level, praxis=praxis)
        # session = SessionLocal()
        # session.add(schema)
        # session.commit()
        # session.close()
        return True
#TESTS (THIS IS ASSUMING THAT OCR PROCESSING HAS ALREADY BEEN DONE CORRECTLY)