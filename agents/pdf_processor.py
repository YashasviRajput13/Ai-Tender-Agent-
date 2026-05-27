# pdf_processor.py — TenderIQ PDF Text Extractor

import fitz    # PyMuPDF
import re
import os


def extract_text_from_pdf(pdf_path: str) -> dict:
    """
    Extract all text and metadata from a PDF file.
    Returns a dict with full_text, pages, page_count, metadata, hints.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    result = {
        "full_text"    : "",
        "pages"        : [],
        "page_count"   : 0,
        "metadata"     : {},
        "file_size_kb" : round(os.path.getsize(pdf_path) / 1024, 1),
        "hints"        : {},
    }

    # Open PDF and extract text page by page
    doc   = fitz.open(pdf_path)
    pages = []

    result["page_count"] = len(doc)
    result["metadata"]   = {
        "title"  : doc.metadata.get("title",   ""),
        "author" : doc.metadata.get("author",  ""),
        "subject": doc.metadata.get("subject", ""),
    }

    for page in doc:
        pages.append(page.get_text("text"))

    doc.close()

    result["pages"]     = pages
    result["full_text"] = "\n\n".join(pages)
    result["hints"]     = detect_hints(result["full_text"])

    return result


def detect_hints(text: str) -> dict:
    """
    Auto-detect budget, deadline, and tech skill hints using regex.
    These hints help the AI agent be more accurate.
    """
    hints = {
        "budget_hints"   : [],
        "deadline_hints" : [],
        "skill_hints"    : [],
    }

    # Budget patterns
    for pattern in [
        r"(?:budget|cost|amount|value)[:\s]+(?:Rs\.?|INR|USD|\$|₹)?\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore|million|billion)s?)?",
        r"(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d+)?(?:\s*(?:lakh|crore)s?)?",
        r"\$\s*[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|thousand))?",
    ]:
        found = re.findall(pattern, text, re.IGNORECASE)
        hints["budget_hints"].extend([f.strip() for f in found[:3]])

    # Deadline patterns
    for pattern in [
        r"(?:deadline|due date|last date|closing date|submission)[:\s]+[\w\s,]+\d{4}",
        r"\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}",
        r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}",
    ]:
        found = re.findall(pattern, text, re.IGNORECASE)
        hints["deadline_hints"].extend([f.strip() for f in found[:3]])

    # Tech keyword scan
    keywords = [
        "Python", "React", "Angular", "Vue", "Node.js", "Java",
        "AWS", "Azure", "GCP", "Cloud", "IoT", "AI", "ML",
        "Machine Learning", "Blockchain", "Docker", "Kubernetes",
        "DevOps", "API", "REST", "Mobile", "Android", "iOS",
        "Flutter", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        "Data Analytics", "Power BI", "SAP", "ERP", "5G",
        "Computer Vision", "Deep Learning", "NLP", "Microservices",
    ]
    for kw in keywords:
        if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
            hints["skill_hints"].append(kw)

    return hints


def truncate_for_ai(text: str, max_chars: int = 6000) -> str:
    """
    Trim text to fit AI context window.
    Keeps first half + last half (most important parts of tender docs).
    """
    if len(text) <= max_chars:
        return text

    half = max_chars // 2
    return (
        text[:half]
        + "\n\n... [middle truncated] ...\n\n"
        + text[-half:]
    )