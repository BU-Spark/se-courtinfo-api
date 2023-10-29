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

def get_defen_adr(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the defendant's address.
    '''
    defen_adr = re.search(r'Defendant Address:\s*(.+)', text)
    if defen_adr:
        return defen_adr.group(1)
    else:
        return None

def get_defen_DOB(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the defendant's date of birth.
    '''
    defen_DOB = re.search(r'Defendant DOB:\s*(.+)', text)
    if defen_DOB:
        return defen_DOB.group(1)
    else:
        return None
    
def get_court_name_adr(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the court name and address.
    '''
    court_name_adr = re.search(r'Court Name and Address:\s*(.+)', text)
    if court_name_adr:
        return court_name_adr.group(1)
    else:
        return None

def get_complaint_issued_date(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the complaint issued date.
    '''
    complaint_issued_date = re.search(r'Complaint Issued Date:\s*(.+)', text)
    if complaint_issued_date:
        return complaint_issued_date.group(1)
    else:
        return None

def get_offense_date(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the offense date.
    '''
    offense_date = re.search(r'Offense Date:\s*(.+)', text)
    if offense_date:
        return offense_date.group(1)
    else:
        return None

def get_arrest_date(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the arrest date.
    '''
    arrest_date = re.search(r'Arrest Date:\s*(.+)', text)
    if arrest_date:
        return arrest_date.group(1)
    else:
        return None

def get_next_event_date(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the next event date.
    '''
    next_event_date = re.search(r'Next Event Date:\s*(.+)', text)
    if next_event_date:
        return next_event_date.group(1)
    else:
        return None

def get_police_incident_num(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the police incident number.
    '''
    police_incident_num = re.search(r'Police Incident #:\s*(.+)', text)
    if police_incident_num:
        return police_incident_num.group(1)
    else:
        return None

def get_OBTN(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the OBTN.
    '''
    OBTN = re.search(r'OBTN:\s*(.+)', text)
    if OBTN:
        return OBTN.group(1)
    else:
        return None

def get_offense_codes(text: str) -> Optional[str]:
    '''
    This function takes in the text from the image and returns the offense codes.
    '''
    offense_codes = re.search(r'Offense Codes:\s*(.+)', text)
    if offense_codes:
        return offense_codes.group(1)
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
    complaint_issued_date = get_complaint_issued_date(text)
    offense_date = get_offense_date(text)
    arrest_date = get_arrest_date(text)
    next_event_date = get_next_event_date(text)
    court_name_adr = get_court_name_adr(text)
    police_incident_num = get_police_incident_num(text)
    OBTN = get_OBTN(text)
    offense_codes = get_offense_codes(text)
    raw_text = text
    return CriminalComplaintBase(docket=docket, defen_name=defen_name, defen_adr=defen_adr, 
                                 defen_DOB=defen_DOB, complaint_issued_date=complaint_issued_date, 
                                 offense_date=offense_date, arrest_date=arrest_date, 
                                 next_event_date=next_event_date, court_name_adr=court_name_adr, 
                                 police_incident_num=police_incident_num, OBTN=OBTN, offense_codes=offense_codes,
                                 raw_text=raw_text)

#def fit_schema(text: str):
#    if text




