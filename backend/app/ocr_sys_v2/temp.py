#placeholder
import re
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

from app.ocr_sys_v2.process import *

def process_doc(image: str) -> Optional[str]:
    subscription_key = os.environ["VISION_KEY"]
    endpoint = os.environ["VISION_ENDPOINT"]
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    return read_text(image, computervision_client)

def parse_doc(image: str) -> List[str]:
    text = process_doc(image)
    


