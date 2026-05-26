import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import fitz
import pdfplumber
import requests


def download_pdf(url: str, dest_folder: str = "./tmp") -> str:
    Path(dest_folder).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(url.split("?")[0]) or "tender.pdf"
    destination = os.path.join(dest_folder, filename)
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    with open(destination, "wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            handle.write(chunk)
    return destination


def extract_text_from_pdf(path: str) -> Dict[str, Optional[str]]:
    text = []
    with fitz.open(path) as pdf:
        for page in pdf:
            text.append(page.get_text())

    return {"path": path, "text": "\n\n".join(text), "pages": len(pdf)}


def find_section(text: str, header: str) -> str:
    pattern = rf"{header}[:\s]+(.+?)(?=\n[A-Z][A-Za-z ]+?:|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_sections(text: str) -> Dict[str, List[str]]:
    return {
        "eligibility": [item.strip() for item in re.findall(r"(?m)^\s*[-•]\s*(.+)$", find_section(text, "Eligibility"))],
        "scope_of_work": [item.strip() for item in re.findall(r"(?m)^\s*[-•]\s*(.+)$", find_section(text, "Scope of Work"))],
        "budget": [find_section(text, "Budget")],
        "emd": [find_section(text, "EMD")],
        "technical_requirements": [item.strip() for item in re.findall(r"(?m)^\s*[-•]\s*(.+)$", find_section(text, "Technical Requirements"))],
        "deadlines": [find_section(text, "Deadline")],
        "required_documents": [item.strip() for item in re.findall(r"(?m)^\s*[-•]\s*(.+)$", find_section(text, "Required Documents"))],
    }


def extract_pdf_metadata(path: str) -> Dict[str, Optional[str]]:
    with fitz.open(path) as pdf:
        info = pdf.metadata
    return {
        "title": info.get("title"),
        "author": info.get("author"),
        "creation_date": str(info.get("creationDate")) if info.get("creationDate") else None,
    }


def process_pdf(url: str, dest_folder: str = "./tmp") -> Dict[str, Any]:
    file_path = download_pdf(url, dest_folder=dest_folder)
    extracted = extract_text_from_pdf(file_path)
    sections = parse_sections(extracted["text"])
    metadata = extract_pdf_metadata(file_path)
    return {
        "url": url,
        "filename": os.path.basename(file_path),
        "raw_text": extracted["text"],
        "parsed_sections": {**sections, **metadata},
    }
