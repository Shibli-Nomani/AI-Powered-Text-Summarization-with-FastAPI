# main.py
from fastapi import FastAPI
import uvicorn

# import routers
from endpoints.health import router as health_router

from endpoints.transcript_upload import router as add_transcript_router
from endpoints.logs import router as logs_router
from endpoints.transcript_clean import router as clean_transcript_router
from endpoints.summary import router as summary_router
#from endpoints.query import router as query_router

# Initialize FastAPI app
app = FastAPI(title="AI-Powered Multi-Agent Video Transcript Summarization and Q&A Chatbot")        

# Register all routers
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(add_transcript_router, prefix="/transcript", tags=["Transcript"])
app.include_router(clean_transcript_router, prefix="/clean", tags=["Text Cleaner"])
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
app.include_router(summary_router, prefix="/summary", tags=["Summary"])
#app.include_router(query_router, prefix="/query", tags=["Query"])

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    unicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)




