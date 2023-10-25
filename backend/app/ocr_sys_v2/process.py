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

#NEEDS TO BE EDITED
def read_text(image: str, computervision_client: ComputerVisionClient) -> Optional[str]:
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

    # Print the detected text, line by line
    #edit this
    if read_result.status == OperationStatusCodes.succeeded:
        return read_result
    else:
        return None
        