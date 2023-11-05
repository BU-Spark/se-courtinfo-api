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
from dotenv import load_dotenv
load_dotenv()

#NEEDS TO BE EDITED
def read_text(image: str, endpoint: str, api_key: str) -> Optional[str]:
    credential = AzureKeyCredential(api_key)
    document_client = DocumentAnalysisClient(endpoint, credential)

    with open(image, "rb") as image_stream:
        poller = document_client.begin_recognize_content(form=image_stream)
        result = poller.result()

    # Process the result to extract text
    extracted_text = ""
    for page in result:
        for line in page.lines:
            extracted_text += line.text + "\n"
    
    return extracted_text

def parse_doc(image: str, endpoint: str, api_key: str) -> Optional[str]:
    extracted_text = read_text(image, endpoint, api_key)
    return extracted_text

# Example usage
api_key = os.environ.get("VISION_KEY")
endpoint = os.environ.get("VISION_ENDPOINT")
image_path = "./test_images/test_ddi.jpg"
print(parse_doc(image_path, endpoint, api_key))
        