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
from app.ocr_sys_v2.ddi_schemify import ddi_schema_fill
load_dotenv()

#NEEDS TO BE EDITED
def read_text(image: str) -> Optional[str]:
    api_key = os.environ.get("VISION_KEY")
    endpoint = os.environ.get("VISION_ENDPOINT")
    credential = AzureKeyCredential(api_key)
    document_client = DocumentAnalysisClient(endpoint, credential)

    with open(image, "rb") as image_stream:
        poller = document_client.begin_analyze_document("courtinfo-1", document=image_stream)
        result = poller.result()

    result_json = result.to_dict()
    # Save the result to a JSON file
    with open('backend/app/ocr_sys_v2/test_output.json', "w") as json_file:
        json.dump(result_json, json_file, indent=4)
    
    #dummy response
    #call schemify
    response = ddi_schema_fill()
    
    if response == False:
        response_data = {"message": "Error!"}
    else:
        response_data = {"message": "Success!"}
    
    response = json.dumps(response_data).encode('utf-8')
    print(response)

    return response



image_path = os.path.abspath('backend/app/ocr_sys_v2/test_images/test_ddi.jpg')
read_text(image_path)
