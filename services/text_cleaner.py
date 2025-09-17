# regex patterns and functions for cleaning and normalizing text data
import re

# Clean and normalize text by removing timestamps, page numbers, extra spaces, and special characters
def clean_text(text: str) -> str:
    if not text:
        return ""

    try:
        # Remove timestamps like [00:01:23], (00:01), etc.
        text = re.sub(r"\[?\(?\d{1,2}:\d{2}(?::\d{2}(?:\.\d{1,3})?)?\)?\]?", "", text)

        # Remove page numbers: lines with only digits or "Page X of Y"
        text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"Page\s*\d+(\s*of\s*\d+)?", "", text, flags=re.IGNORECASE)

        # Normalize quotes and dashes
        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        text = text.replace("–", "-").replace("—", "-").replace("…", "...")

        # Remove extra spaces, newlines, non-printable characters
        text = re.sub(r"[^\x20-\x7E]+", " ", text)  # non-printable → space
        text = re.sub(r"\s+", " ", text)

        # Collapse repeated punctuation
        text = re.sub(r"([.!?]){2,}", r"\1", text)

        # Remove space before punctuation
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)

        return text.strip()

    except Exception as e:
        print(f"[ERROR] Cleaning text failed: {e}")
        return text.strip()
