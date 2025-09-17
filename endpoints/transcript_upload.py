# endpoints/add_transcript.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.logs import metadata_log_server
from services.file_processing.file_to_text import FileToText

# Create a router for all transcript upload routes
router = APIRouter(prefix="/transcript", tags=["Transcript"])


@router.post("/upload")
async def upload_transcript(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()
        filename = file.filename

        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # Use FileToText to extract transcript
        transcript = FileToText.extract_text(content, filename)
        transcript_length = len(transcript)

        # Log metadata
        metadata = {
            "file_name": filename,
            "size_bytes": len(content),
            "status": "preprocessed",
            "transcript_length": transcript_length,
            "transcript": transcript,
        }
        unique_file_id = metadata_log_server.log_metadata(metadata)

        return JSONResponse(
            status_code=200,
            content={
                "message": f"Transcript extracted successfully for {filename}",
                "file_name": filename,
                "file_id": unique_file_id,
                "transcript": transcript,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")
