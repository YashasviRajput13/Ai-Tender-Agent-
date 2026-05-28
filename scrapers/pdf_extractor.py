import io
from typing import Tuple
from urllib.parse import urlparse

import httpx

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import fitz
except ImportError:
    fitz = None


def ensure_pdf_libraries() -> None:
    if pdfplumber is None and fitz is None:
        raise RuntimeError("Missing pdf extraction libraries: install pdfplumber or PyMuPDF.")


async def download_pdf_bytes(url: str, client: httpx.AsyncClient) -> bytes:
    response = await client.get(url, timeout=60)
    response.raise_for_status()
    return response.content


def normalize_filename(url: str) -> str:
    parsed = urlparse(url)
    filename = parsed.path.rsplit("/", 1)[-1] or "document.pdf"
    if not filename.lower().endswith(".pdf"):
        filename = f"{filename}.pdf"
    return filename


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text_chunks: list[str] = []
    if pdfplumber is not None:
        try:
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    content = page.extract_text()
                    if content:
                        text_chunks.append(content)
        except Exception:
            pass

    if not text_chunks and fitz is not None:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                content = page.get_text()
                if content:
                    text_chunks.append(content)
        except Exception:
            pass

    return "\n\n".join(text_chunks).strip()


async def download_and_extract_pdf(url: str, client: httpx.AsyncClient) -> Tuple[str, str]:
    ensure_pdf_libraries()
    pdf_bytes = await download_pdf_bytes(url, client)
    filename = normalize_filename(url)
    text = extract_text_from_pdf_bytes(pdf_bytes)
    return text, filename
