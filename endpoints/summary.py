# endpoints/summary_endpoint.py
from fastapi import APIRouter, HTTPException
from schemas.schema import SummaryResponse
from services.graph import build_graph
import asyncio
from aiocache import Cache

# Create API router with prefix /summary and tag Summary (for docs)
router = APIRouter(prefix="/summary", tags=["Summary"])

# Build your LangGraph workflow graph
compiled_graph = build_graph()

# Initialize in-memory cache
cache = Cache(Cache.MEMORY)


@router.post("/", response_model=SummaryResponse)
async def generate_summary(file_id: str):
    """
    Generate a summary for a given file_id using the LangGraph workflow.
    It's a file_name in logs. Example: "Emerging Technology(2).docx"
    Args:
        file_id (str): The file name to summarize.

    Returns:
        SummaryResponse: Object containing the generated summary.
    """
    try:
        # Check cache first
        cached_summary = await cache.get(file_id)
        if cached_summary:
            return SummaryResponse(summary=cached_summary)

        # Prepare initial state for the graph
        state = {"file_id": file_id, "answer": "", "status": ""}

        # Invoke the graph asynchronously
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, compiled_graph.invoke, state)

        if not result or not result.get("answer"):
            raise HTTPException(status_code=404, detail="Summary could not be generated.")

        summary = result["answer"]

        # Store in cache for future requests
        await cache.set(file_id, summary, ttl=3600)  # cache for 1 hour

        return SummaryResponse(summary=summary)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
