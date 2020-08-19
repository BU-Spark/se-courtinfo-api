import pytesseract
from PIL import Image


def extract_document_text(file: str) -> str:
    """
    Takes a python PIL image and runs it against tesseract OCR
    :param file: string representing the path to the image
    :type file: str
    :return: A string representing the text of the document
    :rtype: str
    """
    text = pytesseract.image_to_string(Image.open(file))
    return text
