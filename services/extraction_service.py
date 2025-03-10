import fitz
import easyocr

def extract_text_from_pdf(file_bytes):
    text = ""
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_image(file_bytes):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_bytes, detail=0)
    return ' '.join(result)
