from typing import Dict
import google.cloud.documentai_v1beta3 as documentai

from backend.app.schemas.ddi_schemas import DefendantDemoInfoBaseV1

def extract_ddi_v1(doc: documentai.Document) -> DefendantDemoInfoBaseV1:
    # Extract the first zip 
    text: str = doc.text
    index_zip_txt = text.lower().find("zip:")
    zip_txt = text[index_zip_txt+4:index_zip_txt+10].lower().strip()

    pages_doc = extract_page_to_text(doc)
    third_page = pages_doc[3].lower().split('\n')
    sex_txt = ""
    dob_txt = ""
    charges_txt = ""
    rec_txt = ""
    charge_category_txt = ""
    risk_level = 0
    rec_praxis_txt = ""
    race_txt = ""
    for i in range(len(third_page)):
        if "sex:" in third_page[i]:
            sex_txt = third_page[i][4:].strip()
        elif "dob:" in third_page[i]:
            dob_txt = third_page[i][4:].strip()
        elif "charge(s):" in third_page[i]:
            charges_txt = third_page[i][10:].strip()
        elif "recommendation" == third_page[i].strip():
            rec_txt = third_page[i+1]
        elif "primary charge category" == third_page[i].strip():
            charge_category_txt = third_page[i+1]
        elif "risk level" == third_page[i].strip():
            risk_level = int(third_page[i+1].strip())
        elif "the recommendation is" in third_page[i]:
            rec_praxis_txt = third_page[i]
        elif "race:" in third_page[i]:
            race_txt = third_page[i][4:].strip()

    return DefendantDemoInfoBaseV1(
        zip=int(zip_txt),
        race=race_txt,
        sex=sex_txt,
        recommendation=rec_txt,
        primary_charge_category=charge_category_txt,
        risk_level=risk_level,
        rec_with_praxis=rec_praxis_txt,
        charges=charges_txt,
        dob=dob_txt,
    )

def extract_page_to_text(doc: documentai.Document) -> Dict[int, str]:
    doc_pages = {}
    for page in doc.pages:
        text_segments = page.layout.text_anchor.text_segments[0]
        try:
            start_index = int(text_segments.start_index)
        except:
            start_index = 0
        try:
            end_index = int(text_segments.end_index)
        except:
            end_index = 0
        doc_pages[int(page.page_number)] = doc.text[start_index:end_index]
    return doc_pages