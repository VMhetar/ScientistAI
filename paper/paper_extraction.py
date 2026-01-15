"""
This module is to extract text from a PDF.
"""
from pypdf import PdfReader

MAX_PAGES = 50
MAX_CHARS = 120_000

class PDFExtractionError(Exception):
    pass


def extract_text_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)

        if len(reader.pages) == 0:
            raise PDFExtractionError("PDF has no pages")

        if len(reader.pages) > MAX_PAGES:
            raise PDFExtractionError("PDF too large (page limit exceeded)")

        text_chunks = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

        text = "\n".join(text_chunks).strip()

        if not text:
            raise PDFExtractionError("No extractable text found")

        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS]

        return text

    except Exception as e:
        raise PDFExtractionError(str(e))
