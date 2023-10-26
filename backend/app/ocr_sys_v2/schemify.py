#THIS CODE IS NOT TESTED AS OF CURRENT
'''
General Overview of the code in this file:
1. Takes in an image
2. Passes the image into the OCR API
3. Returns the text from the image
4. Passes the text into a function that fills in the appropriate fields for the schema

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
from dotenv import load_dotenv
from PIL import Image
import sys
import time
from app.ocr_sys_v2.ocr_read import *
from app.schemas.cc_schemas import *
from app.schemas.user_schemas import *
from app.schemas.ddi_schemas import *



load_dotenv()
#CREATED A .ENV FILE THAT HAS KEY AND ENDPOINT TO DOCUMENT INTELLIGENCE API

def process_doc(image: str) -> Optional[str]:
    '''
    This function takes in an image and returns the text from the image.
    It passes the image into the OCR API, which returns a JSON object that includes 
    different parameters, including the text.
    '''
    subscription_key = os.environ.get("VISION_KEY")
    endpoint = os.environ.get("VISION_ENDPOINT")
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    return read_text(image, computervision_client)


def parse_doc(image: str) -> Optional[str]:
    '''
    This function takes in an image, processes it, and then extracts the 
    text from the raw json that is outputted.
    It then returns the extracted text.
    '''
    text = process_doc(image)
    if text.status == OperationStatusCodes.succeeded:
        # Extract and return the recognized text
        extracted_text = ""
        for page in text.analyze_result.read_results:
            for line in page.lines:
                extracted_text += line.text + "\n"
        return extracted_text
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
    next_event_date: Optional[str]
    next_event_type: Optional[str]
    next_event_room_session: Optional[str]
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

    pass

def ddi_schema_fill(text: str) -> DefendantDemographicInfoBase:
    pass

#def fit_schema(text: str):
#    if text






