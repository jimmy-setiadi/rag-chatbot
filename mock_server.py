from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Union, Dict, Any, Optional
import uvicorn

app = FastAPI(title="Mock RAG System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Union[str, Dict[str, Any]]]
    session_id: str

class CourseStats(BaseModel):
    total_courses: int
    course_titles: List[str]

@app.post("/api/query", response_model=QueryResponse)
async def mock_query(request: QueryRequest):
    # Mock response with clickable sources
    mock_sources = [
        {
            "text": "Building Towards Computer Use - Lesson 3",
            "link": "https://learn.deeplearning.ai/courses/building-toward-computer-use-with-anthropic/lesson/zrgb6/multimodal-requests"
        },
        {
            "text": "MCP Course - Lesson 1", 
            "link": "https://learn.deeplearning.ai/courses/building-toward-computer-use-with-anthropic/lesson/gi7jq/overview"
        },
        "Some Course - No Link Available"  # String format for testing
    ]
    
    return QueryResponse(
        answer="This is a **mock response** to test clickable source links. The sources below should include clickable links that open lesson videos in new tabs.",
        sources=mock_sources,
        session_id="mock-session-123"
    )

@app.get("/api/courses", response_model=CourseStats)
async def mock_courses():
    return CourseStats(
        total_courses=4,
        course_titles=[
            "Building Towards Computer Use with Anthropic",
            "MCP: Build Rich-Context AI Apps with Anthropic", 
            "Introduction to RAG Systems",
            "Advanced AI Techniques"
        ]
    )

@app.post("/api/new-session")
async def create_new_session():
    """Create a new chat session"""
    import uuid
    return {"session_id": f"mock-session-{uuid.uuid4().hex[:8]}"

# Serve frontend
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
except Exception as e:
    print(f"Warning: Could not mount frontend directory: {e}")
    print("Make sure you're running from the project root directory")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)