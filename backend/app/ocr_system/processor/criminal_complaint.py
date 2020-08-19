import re
from typing import List, Optional, Dict

from app.schemas.cc_schemas import CriminalComplaintBase


def extract_criminal_complaint(raw_text: str) -> CriminalComplaintBase:
    """
    Takes the raw text from the OCR systems and breaks it down into individual fields
    :param raw_text: Entire text output from the OCR system
    :type raw_text: str
    :return: A base schema representing the formatted data
    :rtype: CriminalComplaintBase
    """
    docket_num = find_docket_number(raw_text)
    subject_name = find_full_name(raw_text)
    dates = find_dates(raw_text)
    # the following date variables assume all dates were recorded properly by the scan -- need to fix that assumption
    if 0 < len(dates):
        date_of_birth = dates[0]
    else:
        date_of_birth = None
    # date of issued complaint
    if 1 < len(dates):
        complaint_issued = dates[1]
    else:
        complaint_issued = None
    # date of offense
    if 2 < len(dates):
        doo = dates[2]
    else:
        doo = None
    if 3 < len(dates):
        arrest_date = dates[3]
    else:
        arrest_date = None
    if 4 < len(dates):
        next_event_date = dates[4]
    else:
        next_event_date = None
    # obtn number
    obtn = find_obtn(raw_text)
    # address
    address = find_addresses(raw_text)
    offense_codes = find_codes(raw_text)
    # incident report number
    irn = str(find_indicent_report(raw_text))
    cc_temp = CriminalComplaintBase(docket=docket_num, defen_name=subject_name, defen_DOB=date_of_birth,
                                    complaint_issued_date=complaint_issued, offense_date=doo, arrest_date=arrest_date,
                                    next_event_date=next_event_date, OBTN=obtn,
                                    police_incident_num=irn, court_name_adr=address['court'],
                                    defen_adr=address['defendant'], offense_codes=offense_codes,
                                    raw_text=raw_text
                                    )
    return cc_temp


def find_docket_number(document) -> Optional[str]:
    docket = re.search("[0-9]{4}[A-Z]{2}[0-9]{6}", document)
    if docket is not None:
        return docket.group()
    return None


def find_full_name(document) -> Optional[str]:
    name = re.search("[A-Z][a-z]*\s[A-Z]\s[A-Z][a-z]*", document)
    if name is not None:
        return name.group()
    return None


def find_dates(document) -> Optional[List[str]]:
    dates = re.findall("[0-9]{2}/[0-9]{2}/[0-9]{4}", document)
    if dates is not None:
        return dates
    return None


def find_obtn(document) -> Optional[str]:
    obtn = re.search("[A-Z]{4}[0-9]{9}", document)
    if obtn is not None:
        return obtn.group()
    return None


def find_indicent_report(document) -> Optional[str]:
    # OCR currently interprets initial character as a 1, should really be an I
    irn = re.search("I[0-9]{3}\s[0-9]{3}\s[0-9]{3}", document)
    if irn is not None:
        return irn.group()
    return None


def find_addresses(document) -> Dict[Optional[str], Optional[str]]:
    street = re.findall('[0-9][0-9]*\s[A-Z][a-z]*\s[A-Z][a-z]+', document)
    city_state = re.findall('[A-Z][a-z]+[,]\s[A-Z]{2}\s[0-9]{5}', document)
    if len(street) == 2 and len(city_state) == 2:
        return {'court': street[1] + ' ' + city_state[1], 'defendant': street[0] + ' ' + city_state[0]}
    return {'court': None, 'defendant': None}


def find_codes(document) -> Optional[str]:
    try:
        temp_doc = document[document.index('DESCRIPTION') + len('DESCRIPTION'):]
        codes = re.findall('[1-9]+\s[1-9][0-9]+/?[0-9]{2,}?[A-Z]?/?[A-Z]?', temp_doc)
        for i in range(len(codes)):
            codes[i] = codes[i][2:]
        return str(codes)
    except:
        return None
