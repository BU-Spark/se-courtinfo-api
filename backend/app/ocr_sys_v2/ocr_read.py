'''
General Overview of the code in this file:
1. Takes in an image
2. Passes the image into the OCR API
3. Returns the JSON blob from the OCR API
4. Extracts the text from the JSON blob

The returned code gets processed into either the CC or DDI schema.
'''
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Optional
from array import array
import os
from PIL import Image
import sys
import time
import json
from dotenv import load_dotenv
load_dotenv()

#NEEDS TO BE EDITED
def read_text(image: str, endpoint: str, api_key: str) -> Optional[str]:
    credential = AzureKeyCredential(api_key)
    document_client = DocumentAnalysisClient(endpoint, credential)

    with open(image, "rb") as image_stream:
        poller = document_client.begin_analyze_document("prebuilt-document", document=image_stream)
        result = poller.result()

    result_json = result.to_dict()

    # Save the result to a JSON file
    with open('backend/app/ocr_sys_v2/test_output.json', "w") as json_file:
        json.dump(result_json, json_file, indent=4)
    
    return result


api_key = os.environ.get("VISION_KEY")
endpoint = os.environ.get("VISION_ENDPOINT")
image_path = os.path.abspath('backend/app/ocr_sys_v2/test_images/test_ddi.jpg')
read_text(image_path, endpoint, api_key)
        
'''
EXAMPLE RESULT
AnalyzeResult(api_version=2023-07-31, model_id=prebuilt-document, content=Page 1 of 2
Defendant Demographic Information
Lemy FAKE RECORD Stringbean - PTCC Case #CA10592016123003115700
Basic Information:
Name: Udall Garroway
DOB: 09/16/48
SSN: 791-85-2224
Sex: MRace: White
Age: 73 Birth Place: Virginia U.S.
Primary Language English
SID#: 61-567-6382
Dep Living w/ Defendant: 0
Marital Status: Never Married
Dependents: 0
FBI#:
Local Tracking#:
Notes: Def has pending FTA: Disorderly on 12/1/2021 in Arlington.
Def is on active probation with Dist 29 with Off Smith 10/4/21 DE
Known Aliases: Alias Name
Residence:
Verified By: Not Verified
Homeless: No Fixed Address: Yes Phone: (333) 333-3333
Alias SSN
Alias DOB
Cell Phone:
Addr1: 1600 E St. NW
Addr2:
City:
Washington
State: D.C.
Vehicle Access:
Public Transportation Access:
Notes:
Home Phone:
Email:
Relationship:
Lives With:
Length at Present Address: Years :_ 2
Months: 0
In area: Years: 27
Months:
0
Zip: 23319
In State: Years:
0
Months: 0
Drivers License:
State Issued:
References:
Name
Relationship
Phone Number Note
Barack Obama
Friend
(202) 555-6789
12/30/06 DE ref comp
Employment: Verified By: DE 12/30/06
Employed: Yes
Employer: Fairfax County Government
Phone:
Addr1: trustee/FT/1 yr
City:
Supervisor:
Addr2:
State:
Emp From:
Zip:
Wages:
Period:
'''