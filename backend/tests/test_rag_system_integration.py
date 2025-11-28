#!/usr/bin/env python3
"""Integration tests for RAG system content queries"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from config import config
from rag_system import RAGSystem

@pytest.mark.integration
class TestRAGSystemIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock config to avoid real API calls
        self.mock_config = Mock()
        self.mock_config.CHUNK_SIZE = 1000
        self.mock_config.CHUNK_OVERLAP = 200
        self.mock_config.CHROMA_PATH = "./test_chroma"
        self.mock_config.EMBEDDING_MODEL = "all-MiniLM-L6-v2"
        self.mock_config.MAX_RESULTS = 5
        self.mock_config.ANTHROPIC_API_KEY = "test_key"
        self.mock_config.ANTHROPIC_MODEL = "claude-3-sonnet-20240229"
        self.mock_config.MAX_HISTORY = 10
    
    @patch('rag_system.DocumentProcessor')
    @patch('rag_system.VectorStore')
    @patch('rag_system.AIGenerator')
    @patch('rag_system.SessionManager')
    def test_rag_system_initialization(self, mock_session, mock_ai, mock_vector, mock_doc):
        """Test RAG system initializes correctly"""
        rag_system = RAGSystem(self.mock_config)
        
        # Verify components were initialized
        mock_doc.assert_called_once()
        mock_vector.assert_called_once()
        mock_ai.assert_called_once()
        mock_session.assert_called_once()
        
        # Verify tools were registered
        self.assertIsNotNone(rag_system.tool_manager)
        self.assertIsNotNone(rag_system.search_tool)
        self.assertIsNotNone(rag_system.outline_tool)
    
    @patch('rag_system.DocumentProcessor')
    @patch('rag_system.VectorStore')
    @patch('rag_system.AIGenerator')
    @patch('rag_system.SessionManager')
    def test_query_execution_flow(self, mock_session, mock_ai, mock_vector, mock_doc):
        """Test complete query execution flow"""
        # Set up RAG system
        rag_system = RAGSystem(self.mock_config)
        
        # Mock AI generator response
        mock_ai_instance = mock_ai.return_value
        mock_ai_instance.generate_response.return_value = "AI response about MCP"
        
        # Mock tool manager
        rag_system.tool_manager.get_tool_definitions.return_value = [
            {"name": "search_course_content", "description": "Search tool"}
        ]
        rag_system.tool_manager.get_last_sources.return_value = [
            {"text": "MCP Course - Lesson 1", "link": "http://example.com"}
        ]
        rag_system.tool_manager.reset_sources = Mock()
        
        # Mock session manager
        mock_session_instance = mock_session.return_value
        mock_session_instance.get_conversation_history.return_value = "Previous: Hello"
        mock_session_instance.add_exchange = Mock()
        
        # Execute query
        response, sources = rag_system.query("What is MCP?", "session_123")
        
        # Verify AI generator was called with correct parameters
        mock_ai_instance.generate_response.assert_called_once()
        call_args = mock_ai_instance.generate_response.call_args
        
        self.assertIn("What is MCP?", call_args[1]['query'])
        self.assertEqual(call_args[1]['conversation_history'], "Previous: Hello")
        self.assertIsNotNone(call_args[1]['tools'])
        self.assertEqual(call_args[1]['tool_manager'], rag_system.tool_manager)
        
        # Verify response and sources
        self.assertEqual(response, "AI response about MCP")
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["text"], "MCP Course - Lesson 1")
        
        # Verify session was updated
        mock_session_instance.add_exchange.assert_called_once_with(
            "session_123", "What is MCP?", "AI response about MCP"
        )
    
    @patch('rag_system.DocumentProcessor')
    @patch('rag_system.VectorStore')
    @patch('rag_system.AIGenerator')
    @patch('rag_system.SessionManager')
    def test_query_without_session(self, mock_session, mock_ai, mock_vector, mock_doc):
        """Test query execution without session ID"""
        rag_system = RAGSystem(self.mock_config)
        
        mock_ai_instance = mock_ai.return_value
        mock_ai_instance.generate_response.return_value = "Response without session"
        
        rag_system.tool_manager.get_tool_definitions.return_value = []
        rag_system.tool_manager.get_last_sources.return_value = []
        rag_system.tool_manager.reset_sources = Mock()
        
        response, sources = rag_system.query("Test query")
        
        # Verify no session history was requested
        mock_ai_instance.generate_response.assert_called_once()
        call_args = mock_ai_instance.generate_response.call_args
        self.assertIsNone(call_args[1]['conversation_history'])
        
        self.assertEqual(response, "Response without session")
        self.assertEqual(sources, [])

if __name__ == '__main__':
    unittest.main()