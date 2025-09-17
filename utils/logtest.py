import os
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent  # go up from utils/ to project root
LOG_FILE = BASE_DIR / "logs" / "file_metadata.json"


class TranscriptExtractor:
    """Extracts cleaned transcripts from logs/file_metadata.json."""

    @staticmethod
    def _load_metadata() -> dict:
        if not LOG_FILE.exists():
            print("⚠️ Log file not found:", LOG_FILE)
            return {}
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                print(f"✅ Loaded metadata from {LOG_FILE}, entries: {len(data.get('_default', {}))}")
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError as e:
                print("❌ JSON decode error:", str(e))
                return {}

    @staticmethod
    def _run(file_id: str) -> str:
        print(f"🔎 Running TranscriptExtractor for file_id: {file_id}")

        if not file_id or not isinstance(file_id, str):
            raise ValueError("file_id must be a non-empty string.")

        logs = TranscriptExtractor._load_metadata()
        default_logs = logs.get("_default", {})

        log_entry = next((v for v in default_logs.values() if v.get("file_name") == file_id), None)
        if not log_entry:
            raise ValueError(f"No metadata found for file_id: {file_id}")

        cleaned_text = log_entry.get("cleaned_transcript", "").strip()
        if not cleaned_text:
            raise ValueError(f"No cleaned transcript available for file_id: {file_id}")

        print(f"✅ Extracted transcript length: {len(cleaned_text)} characters")
        return cleaned_text


# Instantiate the extractor
transcript_extractor = TranscriptExtractor()

# Quick test block
if __name__ == "__main__":
    test_file_id = "Emerging Technology(1).docx"  # replace with actual file_name in logs
    try:
        transcript_text = transcript_extractor._run(test_file_id)
        print("\n--- Transcript Preview ---")
        print(transcript_text[:500])  # print first 500 chars
    except Exception as e:
        print("❌ Error during extraction:", str(e))
