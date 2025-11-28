import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from typing import Dict, List, Any

@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    config = Mock()
    config.anthropic_api_key = "test-key"
    config.chroma_db_path = ":memory:"
    return config

@pytest.fixture
def mock_rag_system():
    """Mock RAG system for API testing"""
    rag_system = Mock()
    rag_system.query.return_value = ("Test answer", ["Test source"])
    rag_system.get_course_analytics.return_value = {
        "total_courses": 2,
        "course_titles": ["Course 1", "Course 2"]
    }
    rag_system.get_available_commands.return_value = {
        "search-course": "Search course content",
        "get-outline": "Get course outline"
    }
    rag_system.session_manager.create_session.return_value = "test-session-id"
    return rag_system

@pytest.fixture
def test_client(mock_rag_system):
    """FastAPI test client with mocked dependencies"""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from typing import List, Optional, Union, Dict, Any
    
    # Create test app without static file mounting
    app = FastAPI(title="Test RAG System")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Pydantic models
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
    
    # API endpoints
    @app.post("/api/query", response_model=QueryResponse)
    async def query_documents(request: QueryRequest):
        session_id = request.session_id or mock_rag_system.session_manager.create_session()
        answer, sources = mock_rag_system.query(request.query, session_id)
        return QueryResponse(answer=answer, sources=sources, session_id=session_id)
    
    @app.get("/api/courses", response_model=CourseStats)
    async def get_course_stats():
        analytics = mock_rag_system.get_course_analytics()
        return CourseStats(
            total_courses=analytics["total_courses"],
            course_titles=analytics["course_titles"]
        )
    
    @app.post("/api/new-session")
    async def create_new_session():
        session_id = mock_rag_system.session_manager.create_session()
        return {"session_id": session_id}
    
    @app.get("/api/commands")
    async def get_available_commands():
        commands = mock_rag_system.get_available_commands()
        return {"commands": commands}
    
    return TestClient(app)

@pytest.fixture
def sample_query_data():
    """Sample query request data"""
    return {
        "query": "What is covered in lesson 1?",
        "session_id": "test-session"
    }

@pytest.fixture
def sample_course_data():
    """Sample course analytics data"""
    return {
        "total_courses": 3,
        "course_titles": [
            "MCP: Build Rich-Context AI Apps",
            "Building Computer Use",
            "RAG Fundamentals"
        ]
    }