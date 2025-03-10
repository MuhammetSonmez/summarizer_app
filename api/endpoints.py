from fastapi import APIRouter, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from services.summarizer_service import TextSummarizer
from services.extraction_service import extract_text_from_pdf, extract_text_from_image
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "summary": ""})


@router.post("/", response_class=HTMLResponse)
async def summarize_text(
    request: Request,
    text: str = Form(""),
    num_sentences: int = Form(1),
    file: UploadFile = File(None)
):
    extracted_text = text

    if file:
        file_content = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_content)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            extracted_text = extract_text_from_image(file_content)

    if not extracted_text.strip():
        summary = "No valid text found for summarization."
    else:
        summarizer = TextSummarizer(extracted_text, num_sentences)
        summary = summarizer.summarize()

    return templates.TemplateResponse("index.html", {"request": request, "summary": summary})
