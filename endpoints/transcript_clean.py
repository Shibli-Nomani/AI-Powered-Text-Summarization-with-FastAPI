# endpoints/transcript_clean.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.logs import metadata_log_server
from services.file_processing.clean_text import clean_text

router = APIRouter(prefix="/cleaning", tags=["Text Cleaner"])

# ✅ Create router with prefix and tag for docs grouping
@router.post("/clean")
async def clean_all_transcripts():
    """
    Automatically clean all transcripts that are in 'preprocessed' status.
    Updates the metadata log with 'cleaned_transcript' and changes status to 'cleaned'.
    """
    try:
        logs = metadata_log_server.get_logs()
        if not logs:
            return JSONResponse(
                status_code=200,
                content={"message": "No transcripts found in the metadata log.", "cleaned_files": []}
            )

        cleaned_files = []

        for log_entry in logs:
            file_id = log_entry["file_name"]
            status = log_entry.get("status", "")
            raw_transcript = log_entry.get("transcript", "")

            # Only clean transcripts that are preprocessed and non-empty
            if status == "preprocessed" and raw_transcript.strip():
                cleaned_transcript = clean_text(raw_transcript)
                metadata_log_server.update_log(file_id, {
                    "status": "cleaned",
                    "cleaned_transcript": cleaned_transcript,
                    "cleaned_transcript_length": len(cleaned_transcript)
                })
                cleaned_files.append({"file_id": file_id, "cleaned_length": len(cleaned_transcript)})

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Cleaned {len(cleaned_files)} transcript(s).",
                "cleaned_files": cleaned_files
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcript cleaning error: {str(e)}")
