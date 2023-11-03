'''
General Overview of the code in this file:
1. Takes in an image
2. Passes the image into the OCR API
3. Returns the JSON blob from the OCR API
4. Extracts the text from the JSON blob

The returned code gets processed into either the CC or DDI schema.
'''

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
from dotenv import load_dotenv
load_dotenv()

#NEEDS TO BE EDITED
def read_text(image: str, computervision_client: ComputerVisionClient) -> Optional[str]:
    #CURRENT ISSUE -> UNABLE TO AUTHENTICATE FOLLOWING LINE
    read_response = computervision_client.read(image,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    #edit this
    if read_result.status == OperationStatusCodes.succeeded:
        return read_result
    else:
        return None

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
    print(computervision_client)
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

#TEST
print(process_doc("./test_images/test_ddi.jpg"))
        