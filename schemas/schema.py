# schema.py
from pydantic import BaseModel


class CleanedTranscriptResponse(BaseModel):
    """Response model for returning cleaned transcript text."""
    cleaned_transcript: str


class CleanTranscriptRequest(BaseModel):
    """Request model for cleaning a raw transcript."""
    transcript: str


class QueryRequest(BaseModel):
    """Request model for querying a cleaned transcript."""
    cleaned_transcript: str
    query: str


class SummaryResponse(BaseModel):
    """Response model for returning a generated summary."""
    summary: str
