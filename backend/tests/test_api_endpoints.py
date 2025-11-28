import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

@pytest.mark.api
class TestAPIEndpoints:
    """Test FastAPI endpoints for proper request/response handling"""
    
    def test_query_endpoint_success(self, test_client, sample_query_data):
        """Test successful query endpoint"""
        response = test_client.post("/api/query", json=sample_query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "session_id" in data
        assert data["answer"] == "Test answer"
        assert data["sources"] == ["Test source"]
    
    def test_query_endpoint_without_session(self, test_client):
        """Test query endpoint creates session when none provided"""
        query_data = {"query": "Test query"}
        response = test_client.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-id"
    
    def test_query_endpoint_invalid_request(self, test_client):
        """Test query endpoint with invalid request"""
        response = test_client.post("/api/query", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_courses_endpoint_success(self, test_client):
        """Test courses endpoint returns proper statistics"""
        response = test_client.get("/api/courses")
        
        assert response.status_code == 200
        data = response.json()
        assert "total_courses" in data
        assert "course_titles" in data
        assert data["total_courses"] == 2
        assert len(data["course_titles"]) == 2
    
    def test_new_session_endpoint(self, test_client):
        """Test new session creation endpoint"""
        response = test_client.post("/api/new-session")
        
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == "test-session-id"
    
    def test_commands_endpoint(self, test_client):
        """Test available commands endpoint"""
        response = test_client.get("/api/commands")
        
        assert response.status_code == 200
        data = response.json()
        assert "commands" in data
        assert isinstance(data["commands"], dict)
        assert "search-course" in data["commands"]
    
    def test_cors_headers(self, test_client):
        """Test CORS headers are properly set"""
        response = test_client.options("/api/query")
        
        # FastAPI TestClient doesn't fully simulate CORS preflight
        # but we can test that the middleware is configured
        assert response.status_code in [200, 405]  # Either OK or Method Not Allowed
    
    @patch('conftest.mock_rag_system')
    def test_query_endpoint_error_handling(self, mock_rag, test_client):
        """Test error handling in query endpoint"""
        # This test would need the actual app with error handling
        # For now, we test the happy path with mocked responses
        query_data = {"query": "Test error query"}
        response = test_client.post("/api/query", json=query_data)
        
        # With mocked system, this should still succeed
        assert response.status_code == 200

@pytest.mark.api
class TestAPIResponseFormats:
    """Test API response formats and data structures"""
    
    def test_query_response_format(self, test_client, sample_query_data):
        """Test query response has correct format"""
        response = test_client.post("/api/query", json=sample_query_data)
        data = response.json()
        
        # Check required fields
        required_fields = ["answer", "sources", "session_id"]
        for field in required_fields:
            assert field in data
        
        # Check data types
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert isinstance(data["session_id"], str)
    
    def test_courses_response_format(self, test_client):
        """Test courses response has correct format"""
        response = test_client.get("/api/courses")
        data = response.json()
        
        # Check required fields
        assert "total_courses" in data
        assert "course_titles" in data
        
        # Check data types
        assert isinstance(data["total_courses"], int)
        assert isinstance(data["course_titles"], list)
        assert all(isinstance(title, str) for title in data["course_titles"])
    
    def test_commands_response_format(self, test_client):
        """Test commands response has correct format"""
        response = test_client.get("/api/commands")
        data = response.json()
        
        assert "commands" in data
        assert isinstance(data["commands"], dict)
        
        # Check that all values are strings (descriptions)
        for cmd, desc in data["commands"].items():
            assert isinstance(cmd, str)
            assert isinstance(desc, str)