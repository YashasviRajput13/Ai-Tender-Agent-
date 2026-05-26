from typing import Dict


def extract_text_from_pdf(path: str) -> Dict:
    # Placeholder implementation; integrate with pdfminer or OCR engine.
    return {"path": path, "text": "Detected PDF content.", "pages": 1}


def normalize_pdf_data(raw: Dict) -> Dict:
    return {
        "title": raw.get("title", "Untitled Tender"),
        "requirements": raw.get("requirements", []),
        "summary": raw.get("text", ""),
    }
