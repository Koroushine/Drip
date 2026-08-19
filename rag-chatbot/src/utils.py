# src/utils.py

import os
import re
from typing import List, Optional

# Try PyPDF2, fallback to pdfplumber
try:
    import PyPDF2

    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber

    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


def load_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF file"""
    text = ""

    # Try PyPDF2 first
    if HAS_PYPDF2:
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text:
                return text
        except Exception as e:
            print(f"PyPDF2 error for {pdf_path}: {e}")

    # Fallback to pdfplumber
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text:
                return text
        except Exception as e:
            print(f"pdfplumber error for {pdf_path}: {e}")

    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    # Clean text
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[^\w\s\.\?,!;:\'"]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if overlap > 0 and len(current_chunk) > overlap:
                current_chunk = current_chunk[-overlap:] + sentence + " "
            else:
                current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def truncate_text(text: str, max_length: int = 300) -> str:
    """Truncate text to max_length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def clean_text(text: str) -> str:
    """Clean text for processing"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\?,!;:\'"]+', ' ', text)
    return text.strip()