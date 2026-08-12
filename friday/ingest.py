"""
Handles turning raw course material (PDF / plain text / a web URL) into
clean text, then splitting that text into overlapping chunks ready for
embedding.
"""

import re
import requests
from pypdf import PdfReader
from bs4 import BeautifulSoup

from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n".join(pages)


def extract_text_from_url(url: str) -> str:
    resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # strip elements that are never useful for study content
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    # collapse repeated blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Splits on paragraph/sentence boundaries where possible instead of
    hard character cuts, so a chunk doesn't end mid-formula or mid-idea.
    """
    text = clean_text(text)
    if len(text) <= chunk_size:
        return [text] if text else []

    # Prefer splitting on paragraph breaks first
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current.strip())
            # if a single paragraph is itself too long, hard-split it
            if len(para) > chunk_size:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunks.append(para[start:end].strip())
                    start = end - overlap
                current = ""
            else:
                current = para

    if current:
        chunks.append(current.strip())

    return [c for c in chunks if c]


def process_source(source_type: str, source_path_or_url: str) -> list[str]:
    """
    source_type: "pdf" | "text" | "url"
    Returns a list of text chunks ready to embed.
    """
    if source_type == "pdf":
        raw = extract_text_from_pdf(source_path_or_url)
    elif source_type == "url":
        raw = extract_text_from_url(source_path_or_url)
    elif source_type == "text":
        with open(source_path_or_url, "r", encoding="utf-8") as f:
            raw = f.read()
    else:
        raise ValueError(f"Unknown source_type: {source_type}")

    return chunk_text(raw)
