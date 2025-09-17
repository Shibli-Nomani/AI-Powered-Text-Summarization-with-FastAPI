# services/file_processing/file_to_text.py
import tempfile
import os
from typing import Optional

import PyPDF2
import docx
from PIL import Image
import pytesseract
# import fitz  # Uncomment if using PyMuPDF for PDF OCR


class FileToText:
    """
    Extract text from PDF, Word (.docx), images, and scanned PDFs (OCR).
    """

    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        """
        Main entry point to extract text from a file.
        """
        ext = filename.split(".")[-1].lower()
        tmp_path: Optional[str] = None
        try:
            # Save file to a temporary location
            with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name

            # Dispatch extraction based on extension
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
            # Clean up temporary file
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    @staticmethod
    def _extract_pdf_text(pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF2.
        OCR can be added for scanned PDFs.
        """
        text_output = ""
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_index, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_output += page_text + "\n"
                    else:
                        # Optional: OCR fallback for scanned pages
                        text_output += FileToText._extract_image_text_from_pdf_page(pdf_path, page_index) + "\n"
            return text_output.strip()
        except Exception as e:
            print(f"[ERROR] PDF text extraction failed: {e}")
            return ""

    @staticmethod
    def _extract_docx_text(docx_path: str) -> str:
        """Extract text from DOCX files."""
        try:
            doc = docx.Document(docx_path)
            text_output = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return text_output.strip()
        except Exception as e:
            print(f"[ERROR] DOCX text extraction failed: {e}")
            return ""

    @staticmethod
    def _extract_image_text(image_path: str) -> str:
        """Extract text from images using pytesseract OCR."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"[ERROR] Image OCR failed: {e}")
            return ""

    @staticmethod
    def _extract_image_text_from_pdf_page(pdf_path: str, page_index: int) -> str:
        """
        Optional: OCR fallback for PDF page using PyMuPDF.
        Uncomment import fitz at top if using.
        """
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_index)
            pix = page.get_pixmap()
            tmp_img_path = f"{pdf_path}_{page_index}.png"
            pix.save(tmp_img_path)
            text = FileToText._extract_image_text(tmp_img_path)
            os.remove(tmp_img_path)
            return text
        except ImportError:
            print("[WARN] PyMuPDF not installed, skipping PDF OCR.")
            return ""
        except Exception as e:
            print(f"[ERROR] OCR PDF page failed: {e}")
            return ""
