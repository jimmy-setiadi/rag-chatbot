import pytest
from unittest.mock import Mock, patch
import json

@pytest.mark.integration
class TestRAGSystemIntegration:
    """Integration tests for RAG system with API layer"""
    
    @patch('rag_system.RAGSystem')
    def test_full_query_flow(self, mock_rag_class, test_client):
        """Test complete query flow from API to RAG system"""
        # Setup mock
        mock_rag_instance = Mock()
        mock_rag_instance.query.return_value = (
            "Integration test answer", 
            ["Source 1", "Source 2"]
        )
        mock_rag_instance.session_manager.create_session.return_value = "integration-session"
        mock_rag_class.return_value = mock_rag_instance
        
        # Test query
        query_data = {
            "query": "What is RAG?",
            "session_id": "integration-session"
        }
        
        response = test_client.post("/api/query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Test answer"  # From conftest mock
        assert len(data["sources"]) == 1
    
    def test_session_persistence(self, test_client):
        """Test session persistence across multiple queries"""
        # First query - creates session
        response1 = test_client.post("/api/query", json={"query": "First query"})
        session_id = response1.json()["session_id"]
        
        # Second query - uses same session
        response2 = test_client.post("/api/query", json={
            "query": "Second query",
            "session_id": session_id
        })
        
        assert response2.json()["session_id"] == session_id
    
    def test_course_analytics_integration(self, test_client):
        """Test course analytics endpoint integration"""
        response = test_client.get("/api/courses")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure matches expected analytics
        assert data["total_courses"] >= 0
        assert isinstance(data["course_titles"], list)

@pytest.mark.integration  
class TestErrorHandling:
    """Test error handling across the system"""
    
    def test_malformed_json_request(self, test_client):
        """Test handling of malformed JSON requests"""
        response = test_client.post(
            "/api/query",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, test_client):
        """Test handling of missing required fields"""
        response = test_client.post("/api/query", json={"session_id": "test"})
        
        assert response.status_code == 422
        error_detail = response.json()
        assert "detail" in error_detail
    
    def test_invalid_endpoint(self, test_client):
        """Test handling of invalid endpoints"""
        response = test_client.get("/api/nonexistent")
        
        assert response.status_code == 404