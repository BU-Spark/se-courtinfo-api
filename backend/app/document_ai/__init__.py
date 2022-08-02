import os
import google.cloud.documentai_v1beta3 as documentai
from dotenv import load_dotenv
from backend.app.crud.ddi_crud import create_ddi
from backend.app.ocr_system.processor.ddi_processor import extract_ddi_v1
from app.db.session import SessionLocal

def get_client() -> documentai.DocumentProcessorServiceClient:
    API_LOCATION = 'us'
    client_options = dict(api_endpoint=f"{API_LOCATION}-documentai.googleapis.com")
    return documentai.DocumentProcessorServiceClient(client_options=client_options)

def process_ccf_document(file_path: str, mime_type: str) -> bool:
    load_dotenv()
    client = get_client()
    with open(file_path, "rb") as file:
        document_content = file.read()
    location = "us"
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID', '')
    processor_id = os.getenv('GOOGLE_CLOUD_PROCESSOR_ID', '')
    assert project_id != ''
    assert processor_id != ''
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    document = documentai.RawDocument(content=document_content, mime_type=mime_type)  #MIME_TYPE needs to be checked
    request = documentai.ProcessRequest(raw_document=document, name=processor_name)
    
    # DocumentAI does ocr processing to retrieve the text
    response = client.process_document(request=request)
    doc: documentai.Document = response.document
    
    # Extract the necessary information from the document returned from the API
    ddi_model = extract_ddi_v1(doc)
    db = SessionLocal()
    # Create ddi model to be stored in db
    ddi = create_ddi(db, ddi_model)
    return ddi.ddi_id
 