# services/metadata_log_server.py
import os
from datetime import datetime
from tinydb import TinyDB, Query
from tinydb.operations import set as tdb_set

# ------------------------------
# Setup TinyDB
# ------------------------------
LOG_FILE = "logs/file_metadata.json"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

db = TinyDB(LOG_FILE)

# ------------------------------
# Public API
# ------------------------------
def log_metadata(metadata: dict) -> str:
    """
    Log metadata for uploaded files.
    Ensures unique file_name (used as file_id).
    Returns the unique file_id (file_name).
    """
    if "upload_time" not in metadata:
        metadata["upload_time"] = datetime.utcnow().isoformat()

    # Handle duplicate file_name
    base_name, ext = os.path.splitext(metadata["file_name"])
    existing_names = [log["file_name"] for log in db.all()]
    counter = 1
    unique_file_id = metadata["file_name"]
    while unique_file_id in existing_names:
        unique_file_id = f"{base_name}({counter}){ext}"
        counter += 1
    metadata["file_name"] = unique_file_id

    db.insert(metadata)
    return unique_file_id  # Return the unique file ID


def get_logs() -> list:
    """Retrieve all logged file metadata."""
    return db.all()


def get_log(file_id: str) -> dict:
    """Retrieve metadata for a specific file_id (file_name)."""
    File = Query()
    results = db.search(File.file_name == file_id)
    return results[0] if results else {}


def update_log(file_id: str, updates: dict) -> bool:
    """Update existing log entry by file_id (file_name)."""
    File = Query()
    for key, value in updates.items():
        db.update(tdb_set(key, value), File.file_name == file_id)
    return True


def clear_logs() -> bool:
    """Clears all logs from the database."""
    db.truncate()
    return True
