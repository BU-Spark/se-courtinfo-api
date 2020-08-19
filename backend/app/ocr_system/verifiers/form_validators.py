from typing import Optional

from app.schemas.cc_schemas import CriminalComplaintBase


def verify_cc(cc: CriminalComplaintBase) -> Optional[CriminalComplaintBase]:
    """
    Verifies a Criminal Complaint Form to ensure that it contains the required fields.
    This would typically occur after retrieving the data from the OCR system
    :param cc: Input instance of a CriminalComplaintBase
    :type cc: CriminalComplaintBase
    :return: The passed object or None if 
    :rtype:
    """
    # Currently a pass through since no field requirements have been defined for this form
    return cc
