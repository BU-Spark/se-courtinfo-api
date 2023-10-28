#THIS CODE IS NOT TESTED AS OF CURRENT
'''
General Overview of the code in this file:
1. Gets the parsed text from the image (which has already been passed through the OCR API)
2. Passes the text into a function that fills in the appropriate fields for the cc schema

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


def get_docket(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the docket number.
    '''
    docket = re.search(r'Docket No.:\s*(\d{2}-\w{2}-\d{6})', text)
    if docket:
        return docket.group(1)
    else:
        return None


def get_defen_name(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the defendant's name.
    '''
    defen_name = re.search(r'Defendant Name:\s*(.+)', text)
    if defen_name:
        return defen_name.group(1)
    else:
        return None

# MIGHT PUT THESE INTO 2 SEPARATE FILES  
def cc_schema_fill(text: str) -> CriminalComplaintBase:
    '''
    A Criminal Complaint is made up of the following fields:
    docket: Optional[str]
    number_of_counts: Optional[int]
    defen_name: Optional[str]
    defen_adr: Optional[str]
    defen_DOB: Optional[str]
    court_name_adr: Optional[str]
    complaint_issued_date: Optional[str]
    offense_date: Optional[str]
    arrest_date: Optional[str]
    offense_city: Optional[str]
    offense_adr: Optional[str]
    police_dept: Optional[str]
    police_incident_num: Optional[str]
    OBTN: Optional[str]
    PCF_number: Optional[str]
    defen_xref_id: Optional[str]
    offense_codes: Optional[str]
    raw_text: Optional[str]
    This function takes in the text from the image and fills in the appropriate fields
    for the CriminalComplaintBase schema.
    '''
    docket = get_docket(text)
    defen_name = get_defen_name(text)
    defen_adr = get_defen_adr(text)
    defen_DOB = get_defen_DOB(text)
    court_name_adr = get_court_name_adr(text)
    complaint_issued_date = get_complaint_issued_date(text)
    offense_date = get_offense_date(text)
    arrest_date = get_arrest_date(text)
    offense_city = get_offense_city(text)
    offense_adr = get_offense_adr(text)
    police_dept = get_police_dept(text)
    police_incident_num = get_police_incident_num(text)
    OBTN = get_OBTN(text)
    PCF_number = get_PCF_number(text)
    defen_xref_id = get_defen_xref_id(text)
    offense_codes = get_offense_codes(text)
    return
    #return CriminalComplaintBase(docket=docket, ...)

#def fit_schema(text: str):
#    if text




