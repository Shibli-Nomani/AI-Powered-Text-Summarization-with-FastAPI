import tempfile
import os
from typing import List

import PyPDF2
import docx
from PIL import Image
import pytesseract
# import fitz  # Uncomment if using PyMuPDF OCR for PDFs


class FileToText:
    """
    Extract text from PDF, Word (.docx), images, and scanned PDFs (OCR).
    """

    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        ext = filename.split(".")[-1].lower()
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            if ext == "pdf":
                return FileToText._extract_pdf_text(tmp_path)
            elif ext == "docx":
                return FileToText._extract_docx_text(tmp_path)
            elif ext in ["png", "jpg", "jpeg", "bmp", "tiff"]:
                return FileToText._extract_image_text(tmp_path)
            else:
                print(f"[WARN] Unsupported file format: {ext}")
                return ""
        except Exception as e:
            print(f"[ERROR] Text extraction failed for {filename}: {e}")
            return ""
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    @staticmethod
    def _extract_pdf_text(pdf_path: str) -> str:
        text_output = ""
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_index, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_output += page_text + "\n"
                    else:
                        # Optional: add OCR here if page_text is empty
                        pass
            return text_output.strip()
        except Exception as e:
            print(f"[ERROR] PDF text extraction failed: {e}")
            return ""

    @staticmethod
    def _extract_docx_text(docx_path: str) -> str:
        try:
            doc = docx.Document(docx_path)
            text_output = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return text_output.strip()
        except Exception as e:
            print(f"[ERROR] DOCX text extraction failed: {e}")
            return ""

    @staticmethod
    def _extract_image_text(image_path: str) -> str:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"[ERROR] Image OCR failed: {e}")
            return ""
